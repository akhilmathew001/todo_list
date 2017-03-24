from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from polls.models.choice import Choice
from .models.question import Question
from polls.models.person import Person
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.all()

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/details.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def index(request):
    question = Question.objects.all()
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list':question,
        }
    return HttpResponse(template.render(context,request))

def detail(request,question_id):
    try:
        question = Question.objects.get(pk = question_id)
    except Question.DoesNotExist:
        raise Http404('Question does not exist')
    return render(request,'polls/details.html',{'question':question})

def results(request,question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question':question}
    return render(request, 'polls/results.html', context)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        context = {'question':question, 'error_message':'You did not selected any choice'}
        return render(request, 'polls/details.html', context)
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('results',args=(question_id)))
