from django.shortcuts import render, redirect
from django.views import View
from .models import Comment
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
class CommentCreateView(View):
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            # フォームからコメントを作成するが、userとtweetのidはまだセットしていない
            comment = form.save(commit=False)
            # コメントにuser_idを追加
            comment.user = request.user
            # コメントにtweet_idをURLパラメータから取得して追加
            # URLConfで 'tweets/<int:pk>/comments/' のように設定していると仮定
            comment.tweet_id = kwargs['pk']
            comment.save()
            # コメント投稿後のリダイレクト先へ
            return redirect('Tweets:detail', pk=comment.tweet_id)
        else:
            # フォームが不正な場合の処理。
            return render(request, 'tweets:detail', {'form': form, 'pk': comment.tweet_id})