from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question

class IndexView(generic.ListView):
    template_name = 'poll/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[:5] 


# def index(request):
#     latest_question_list = Question.objects.order_by('-published_date')[:5]
#     context = {
#         'latest_question_list' : latest_question_list,
#     }
#     return render(request, 'poll/index.html', context)

class DetailView(generic.DetailView):
    model = Question
    template_name = 'poll/detail.html'


    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(published_date__lte=timezone.now())
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'poll/detail.html', {'question': question})


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'poll/results.html'
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'poll/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'poll/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('poll:results', args=(question.id,)))

# Create your views here.
