from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView

from .helpers import generate_random_string, send_mail_to_user
from .models import *


class LoginView(APIView):

    def post(self, request):
        response = {
            'status': 500,
            'message': 'Something went wrong'
        }

        try:
            data = request.data

            if data.get('username') is None:
                response = {'message': 'Key username not found!'}
                raise Exception('Key username not found!')

            if data.get('password') is None:
                response = {'message': 'Key password not found!'}
                raise Exception('Key password not found!')

            check_user = User.objects.filter(
                username=data.get('username')).first()

            if check_user is None:
                response = {'message': 'Invalid username, user not found!'}
                raise Exception('Invalid username not found!')

            if not Profile.objects.filter(user=check_user).first().is_verified:
                response = {'message': 'Your profile is not verified!'}
                raise Exception('Profile not verified!')

            user_obj = authenticate(username=data.get(
                'username'), password=data.get('password'))
            if user_obj:
                login(request, user_obj)
                response = {
                    'status': 200,
                    'message': 'Welcome.'
                }
            else:
                response = {
                    'status': 400,
                    'message': 'Invalid password!'
                }
                raise Exception('Invalid password')

        except Exception as e:
            print(e)

        return Response(response)


class RegisterView(APIView):

    def post(self, request):
        response = {
            'status': 500,
            'message': 
            'Something went wrong'
        }

        try:
            data = request.data

            if data.get('username') is None:
                response = {'message': 'Key username not found!'}
                raise Exception('Key username not found!')

            if data.get('password') is None:
                response = {'message': 'Key password not found!'}
                raise Exception('Key password not found!')

            check_user = User.objects.filter(
                username=data.get('username')).first()

            if check_user:
                response = {'message': 'Username already taken!'}
                raise Exception('Username  already taken!')

            user_obj = User.objects.create(email=data.get(
                'username'), username=data.get('username'))
            user_obj.set_password(data.get('password'))
            user_obj.save()

            token = generate_random_string(20)
            Profile.objects.create(user=user_obj, token=token)

            send_mail_to_user(token, data.get('username'))

            response = {
                'message': 'User created!',
                'status': 200
            }

        except Exception as e:
            print(e)

        return Response(response)


class AddCommentView(APIView):

    def post(self, request):
        response = {
            'status': 500,
            'message': 'Something went wrong'
        }

        try:
            data = request.data
            post_id = data['post_id']

            post = BlogModel.objects.get(id=post_id)
            if post is None:
                response = {
                    'status': 500,
                    'message': 'Post not found'
                }

            if data.get('parent'):
                parent = Comment.objects.get(id=data['parent'])
            else:
                parent = None

            Comment.objects.create(
                user=request.user,
                post=post,
                content=data['content'],
                parent=parent
            )

            response = {
                'status': 200,
                'message': 'Comment created'
            }

        except Exception as e:
            print(e)

        return Response(response)


class AddLikeView(LoginRequiredMixin, APIView):
    def post(self, request):
        response = {
            'status': 500,
            'message': 'Something went wrong'
        }

        try:
            data = request.data
            post_id = data['post_id']

            post = BlogModel.objects.get(id=post_id)

            if not post.likes.filter(created_by=request.user).exists():
                like = post.likes.create(created_by=request.user)

                response = {
                    'liked': True,
                    'likes': post.likes.count(),
                    'message': 'Like added!',
                    'status': 200
                }
            else:
                like = post.likes.filter(created_by=request.user).delete()

                response = {
                    'liked': False,
                    'likes': post.likes.count(),
                    'message': 'Like deleted!',
                    'status': 200
                }

        except Exception as e:
            print(e)

        return Response(response)
