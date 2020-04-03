from django.shortcuts import render, HttpResponse
from django import forms
import json
import os
import csv

from make_2017_table import retrieve_state_data

DATA_DIR = os.path.dirname(__file__)
MANUAL_DIR = os.path.join(DATA_DIR, '../data', 'manually_created')

def gen_dropdown(filename):
    '''
    Generates drop down list from a file (e.g. csv).

    Inputs:
        - filename (string): name of file to use as input to drop down
    Outputs:
        - list of drop down options
    '''
    with open(os.path.join(MANUAL_DIR, filename)) as f:
        f.readline()
        col = [tuple(line) for line in csv.reader(f)]
        col.insert(0, ("None", "None"))

    return [x for x in col]

STATES = gen_dropdown('states_abbrev.csv')


class StateForm(forms.Form):
    '''
    Creates a class to contain forms for user input.
    '''
    your_state = forms.ChoiceField(label='Your State', 
        choices=STATES, required=False)
    comparison_state = forms.ChoiceField(label='Comparison State', 
        choices=STATES, required=False)
    all_years = forms.BooleanField(label='Show 1960-2017',
        required=False)
    show_args = forms.BooleanField(label='Show request',
        required=False)


def home(request):
    '''
    Generates an instance of a StateForm on webpage. After user enters
    inputs into form, uses selections to generate tables and graphs.

    Inputs:
        - request: 

    Outputs:
        - renders State Form
    '''
    context = {}
    res = None
    # if this is a POST request we need to process the form date
    if request.method == 'GET':
        # create a form instance and populate it with data from the request:
        form = StateForm(request.GET)
        # check whether it's valid:
        if form.is_valid():
            args = {}
            if form.cleaned_data['your_state']:
                args['your_state'] = form.cleaned_data['your_state']

            if form.cleaned_data['comparison_state']:
                args['comparison_state'] = form.cleaned_data['comparison_state']

            if form.cleaned_data['show_args']:
                context['args'] = json.dumps(args)

            context['all_years'] = False
            if form.cleaned_data['all_years']:
                context['all_years'] = form.cleaned_data['all_years']

            try:
                res = retrieve_state_data(args)

            except Exception as e:
                print('Exception caught')
                bt = traceback.format_exception(*sys.exc_info()[:3])
                context['err'] = """
                An exception was thrown in find_courses:
                <pre>{}
                {}</pre>
                """.format(e, '\n'.join(bt))

                res = None

    else:
        form = StateForm()
    
    if res is None:
        context['result'] = None

    else:
        columns, result = res

        if result and isinstance(result[0], str):
            result = [(r,) for r in result]

        context['result'] = result
        context['columns'] = columns
    
    if args:
        context['image1'] = [''.join(('graphs/2017_', args[i], '.png'))
        for i in args if args[i] != "None"]
        if context['all_years']:
            context['image2'] = [''.join(('graphs/full_yoy_', args[i], '.png'))
            for i in args if args[i] != "None"]
    
    context['form'] = form

    return render(request, 'index.html', context)
