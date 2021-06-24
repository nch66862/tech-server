from django.http.response import HttpResponse
from rest_framework.decorators import action
from techapi.models import TechUser
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseServerError
from rest_framework import status
from django.utils import timezone
import json

class ExampleViewSet(ViewSet):
## Basic fetches
    def retrieve(self, request, pk):
        priority_user = PriorityUser.objects.get(user=request.auth.user)
        affirmations = Affirmation.objects.filter(priority_id=pk)
        for affirmation in affirmations:
            affirmation.is_author = priority_user == affirmation.priority_user
        affirmations_serialized = AffirmationSerializer(affirmations, many=True, context={'request': request})
        return Response(affirmations_serialized.data, status=status.HTTP_200_OK)
    def create(self, request):
        affirmation = Affirmation()
        affirmation.priority_user = PriorityUser.objects.get(user=request.auth.user)
        affirmation.priority_id = request.data['priority_id']
        affirmation.affirmation = request.data['affirmation']
        affirmation.save()
        serializer = AffirmationSerializer(affirmation, many=False, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def destroy(self, request, pk):
        affirmation = Affirmation.objects.get(pk=pk)
        affirmation.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)
    def list(self, request):
## Exclude method
        priorities = Priority.objects.filter(is_public=True).exclude(priority_user__user=request.auth.user)


        # setting custom properties
        for priority in priorities:
            matching_subscriptions = Subscription.objects.filter(creator_id=priority.priority_user_id)
            for subscription in matching_subscriptions:
                if priority_user.id == subscription.subscriber_id:
                    priority.priority_user.subscribed = True
                else:
                    priority.priority_user.subscribed = False

## Serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')

class TechUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model = TechUser
        fields = ('user',)

class AffirmationSerializer(serializers.ModelSerializer):
    priority_user = PriorityUserSerializer(many=False)
    priority = PrioritySerializer(many=False)
    class Meta:
        model = Affirmation
        fields = ('id', 'priority_user', 'priority', 'affirmation', 'created_on', 'is_author')

### Custom Response
        # establish custom variable to send back
        response = {}

        # Find a streak by adding a number to current streak. Start at today. Work backwards until no more histories or a date is skipped.
        todays_date = datetime.date(datetime.today())
        comparison_date = todays_date
        last_date = None
        current_streak = 0
        current_user = PriorityUser.objects.get(user=request.auth.user)
        # Sort by the date - newest first
        histories = History.objects.filter(
            what__priority__priority_user=current_user).order_by('-goal_date')
        for history in histories:
            # Have to have this initial check for multiple entries in the same day
            if history.goal_date == last_date:
                None
            # Counts up and sets the next date when the streak continues
            elif history.goal_date == comparison_date:
                current_streak += 1
                comparison_date = comparison_date - timedelta(days=1)
                last_date = history.goal_date
            # Breaks out of the loop if the streak ends
            else:
                break
        # Add the streak to the response
        response['current_streak'] = current_streak

        # Filter the history for the current user data only. limit to data only in the past week. total up the time for this data.
        seven_day_time_spent = History.objects.filter(what__priority__priority_user=current_user, goal_date__range=[
                                                      todays_date-timedelta(days=6), todays_date]).aggregate(week_total=Sum('time_spent'))
        week_total_dict = WeekTotalSerializer(
            seven_day_time_spent, many=False, context={'request': request}).data
        response['week_total'] = week_total_dict['week_total']

        # Filter the history for the current user data only. limit to data only in the past week. total up the time for this data.
        total_time_query = History.objects.filter(
            what__priority__priority_user=current_user).aggregate(total_time=Sum('time_spent'))
        total_time_dict = TotalTimeSerializer(
            total_time_query, many=False, context={'request': request}).data
        response['total_time'] = total_time_dict['total_time']

        # Set up the data structure that chart.js needs
        response['line_chart'] = {
            'data': {
                'labels': [],
                'datasets': [{
                    'label': 'time',
                    'data': [],
                    'color': ['black'],
                    'borderColor': ['black'],
                    'borderWidth': 1
                }]
            }
        }
        # put all of the dates in for the labels along the x-axis of the line chart
        for day_offset in range(7):
            response['line_chart']['data']['labels'].append(
                todays_date - timedelta(days=day_offset))
        # query to get the time every day and add that y value for each x value
        for day in response['line_chart']['data']['labels']:
            time_today_query = History.objects.filter(
                what__priority__priority_user=current_user, goal_date=day).aggregate(time_today=Sum('time_spent'))
            time_today_dict = TimeTodaySerializer(
                time_today_query, many=False, context={'request': request}).data
            if time_today_dict['time_today'] is not None:
                response['line_chart']['data']['datasets'][0]['data'].append(
                    time_today_dict['time_today'])
            else:
                response['line_chart']['data']['datasets'][0]['data'].append(0)

        Response(response, status=status.HTTP_200_OK)

## Auth User Info
    priority_user = PriorityUser.objects.get(user = request.auth.user)
    data = json.dumps({"is_active": request.auth.user.is_active, "is_admin": request.auth.user.is_staff, "logged_in_user_id": priority_user.id})
    HttpResponse(data, content_type='application/json')

#another flatter custom data type
            try:
            priority = Priority.objects.get(pk=pk)
            priority_serialized = PrioritySerializer(priority, context={'request': request})
            user = PriorityUser.objects.get(pk=priority.priority_user_id)
            user_serialized = PriorityUserSerializer(user, context={'request': request})
            histories = History.objects.filter(what__priority_id=priority.id)
            history_serialized = HistorySerializer(histories, many=True, context={'request': request})
            response = {}
            response['user'] = user_serialized.data
            response['priority'] = priority_serialized.data
            response['history'] = history_serialized.data
            Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)
