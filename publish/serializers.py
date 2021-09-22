from rest_framework import serializers
from .models import *
from media.models import User, Page, Group
from media.serializers import UserSerializer

class PageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Page
        fields = ('id', 'page_name', 'page_photo')

class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'group_name')


class SnippetSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only = True)
    ReactsCount = serializers.SerializerMethodField(method_name = 'ReactsCount')

    def ReactsCount(self, comment):
        return comment.reacts_count()

    class Meta:
        model = Comment
        fields = ('author', 'id', 'post', 'content', 'DatePublished')


class PostFilesSerializers(serializers.ModelSerializer):

    class Meta:
        model = PostFiles
        fields = ('id', 'content', 'media')

class SharedPostSerializer(serializers.ModelSerializer):
    files = PostFilesSerializers(many = True, source = 'post_file' , read_only = True)
    author = UserSerializer(read_only = True)

    class Meta:
        model = Post
        fields = ('id', 'author', 'page', 'group', 'files', 'content', 'DatePublished')

class PostSerializer(serializers.ModelSerializer):
    files = PostFilesSerializers(many = True, source = 'post_file', read_only = True)
    author = UserSerializer(read_only = True)
    page = PageSerializer(read_only = True)
    group = GroupSerializer(read_only = True)
    ReactsCounter = serializers.SerializerMethodField(method_name = 'ReactsCount')
    SharesCounter = serializers.SerializerMethodField(method_name = 'SharesCount')
    CommentsCounter = serializers.SerializerMethodField(method_name = 'CommentsCount')
    share = SharedPostSerializer(read_only = True)
    checking_per = serializers.SerializerMethodField(method_name = 'checking_perm')
    checking_reactions = serializers.SerializerMethodField(method_name = 'checking_react')
    checking_shares = serializers.SerializerMethodField(method_name = 'checking_share')
    DatePublished = serializers.SerializerMethodField(method_name = 'getDate')

    def getDate(self, post):
        return post.date()

    def ReactsCount(self, post):
        return post.reacts_count()

    def SharesCount(self, post):
        return post.shared_post.count()

    def CommentsCount(self, post):
        return post.comments.count()

    def checking_perm(self, post):
        visitor = self.context['request'].user
        if visitor == post.author:
            return True
        else:
            return False

    def checking_react(self, post):
        visitor = self.context['request'].user
        if visitor in post.likes.all():
            return "fas fa-thumbs-up react"

        elif visitor in post.love.all():
            return "fas fa-heart react"

        elif visitor in post.haha.all():
            return "fas fa-smile react"

        elif visitor in post.sad.all():
            return "fas fa-frown react"

        elif visitor in post.wow.all():
            return "fas fa-surprise react"

        elif visitor in post.angry.all():
            return "fas fa-angry react"

        else:
            return "far fa-thumbs-up react"

    def checking_share(self, post):
        visitor = self.context['request'].user
        shared = Post.objects.filter(share=post, author=visitor)
        if shared:
            return "fas fa-share"
        else:
            return "far fa-share"



    class Meta:
        model = Post
        fields = ('id', 'author', 'share', 'checking_per', 'checking_reactions', 'checking_shares', 'page', 'group', 'files', 'content', 'ReactsCounter', 'SharesCounter', 'CommentsCounter', 'DatePublished')

