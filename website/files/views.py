import json
import base64
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import plotly.express as px
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count
import plotly.graph_objects as go


def index(request):
    return render(request, 'index.html', {})

def CN(request):
    return render(request, 'CN.html', {})


from .models import Project, AuthorDetails, Publication, PublicationDetails  

class NumpyEncoder(json.JSONEncoder):
    """ Custom encoder for numpy data types """
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

def update_plot(author_name, author_position):
    participation_year = AuthorDetails.objects.filter(authorname=author_name).values_list('attended_date', flat=True).first()

    data_before = Publication.objects.filter(author__authorname=author_name, publication_year__lt=participation_year)
    data_after = Publication.objects.filter(author__authorname=author_name, publication_year__gte=participation_year)


    # Apply filters based on author position if needed
    if author_position == 'First Author':
        data_before = data_before.filter(authors__startswith=author_name)
        data_after = data_after.filter(authors__startswith=author_name)
    elif author_position == 'Last Author':
        data_before = data_before.filter(authors__endswith=author_name)
        data_after = data_after.filter(authors__endswith=author_name)

    # Count publications per year
    pub_counts_before = data_before.values('publication_year').annotate(count=Count('publication_id')).order_by('publication_year')
    pub_counts_after = data_after.values('publication_year').annotate(count=Count('publication_id')).order_by('publication_year')

    # Generate plots for both time periods
    figs = {
        'before': generate_bar_fig(list(pub_counts_before), author_name),
        'after': generate_bar_fig(list(pub_counts_after), author_name)
    }

    return figs

def generate_bar_fig(plot_data, author_name):
    if not plot_data:  
        fig = go.Figure()

        # Add text annotation to the middle of the figure
        fig.add_annotation(
            x=0.5,
            y=0.5,
            xref="paper",
            yref="paper",
            text="No data available",
            showarrow=False,
            font=dict(
                size=28,
                color="Black"
            ),
            align="center"
        )

        # Update layout to add title and remove axes
        fig.update_layout(
            title=f"{author_name} - Number of Publications vs Year",
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(showgrid=False, showticklabels=False, zeroline=False)
        )

        return fig.to_dict()
    else:
        # Create bar plot
        bar_fig = px.bar(
            plot_data,
            x='publication_year',
            y='count',
            labels={'publication_year': 'Year', 'count': 'Publication Count'},
            text='count'
        )

        # Calculate the average and round to the nearest whole number
        avg_publications_per_year = round(np.mean([data['count'] for data in plot_data]), 0)
        y_range_max = max([data['count'] for data in plot_data]) + 5

        # Update the layout of the bar figure
        bar_fig.update_layout(
            title=f"{author_name} - Number of Publications vs Year (Average: {avg_publications_per_year})",
            xaxis=dict(title='Year', tickmode='array', tickvals=[data['publication_year'] for data in plot_data], type='category'),
            yaxis=dict(title='Publication Count', range=[0, y_range_max]),
            showlegend=False
        )

        bar_fig.update_traces(
            textposition='inside',
            textangle=0,
        )
    

        return bar_fig.to_dict()


def SG(request):
    main_dropdown_options = list(AuthorDetails.objects.order_by('authorname').values_list('authorname', flat=True).distinct())
    third_dropdown_options = ['All', 'First Author', 'Last Author']

    # If it's an AJAX request, update and return the plot data
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        author_name = request.GET.get('author', main_dropdown_options[0])
        author_position = request.GET.get('position', third_dropdown_options[0])
        plot_data = update_plot(author_name, author_position)
        return JsonResponse(plot_data, encoder=NumpyEncoder)

    return render(request, 'SG.html', {
        'main_dropdown_options': main_dropdown_options,
        'third_dropdown_options': third_dropdown_options,
    })

   


def generate_wordcloud(abstracts):
    if not abstracts:
        fig = go.Figure()

        # Add text annotation to the middle of the figure
        fig.add_annotation(
            x=0.5,
            y=0.5,
            xref="paper",
            yref="paper",
            text="No data available",
            showarrow=False,
            font=dict(
                size=28,
                color="Black"
            ),
            align="center"
        )


        fig.update_layout(
            margin=dict(t=40, b=40, l=80, r=80),
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(showgrid=False, showticklabels=False, zeroline=False)
        )

        return fig.to_dict()

    all_abstracts = ' '.join(abstracts)
    wordcloud = WordCloud(width=400, height=400, background_color='white', max_words=100,collocations=False).generate(all_abstracts)
    img_buffer = BytesIO()
    plt.figure(figsize=(4, 4), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    wordcloud_data = base64.b64encode(img_buffer.read()).decode()
    return wordcloud_data


def filternan(abstracts):
    return [abstract for abstract in abstracts if abstract and str(abstract).lower() != 'nan']

def TE(request):
    if request.method == 'POST':
        selected_author = request.POST.get('selected_author')
        author_participation_year = AuthorDetails.objects.filter(authorname=selected_author).values_list('attended_date', flat=True).first()

        if author_participation_year is not None:
            selected_author_data = Publication.objects.filter(author__authorname=selected_author)

            abstracts_before= selected_author_data.filter(publication_year__lt=author_participation_year).values_list('publicationdetails__abstract', flat=True)
            abstracts_after= selected_author_data.filter(publication_year__gte=author_participation_year).values_list('publicationdetails__abstract', flat=True)

            wordcloud_before = generate_wordcloud(filternan(abstracts_before))
            wordcloud_after = generate_wordcloud(filternan(abstracts_after))

            return JsonResponse({
                'wordcloud_before': wordcloud_before,
                'wordcloud_after': wordcloud_after,
            })
        else:
            return JsonResponse({
                'error': 'Author participation year not available.'
            })

    else:
        author_list = AuthorDetails.objects.order_by('authorname').values_list('authorname', flat=True).distinct()
        return render(request, 'TE.html', {'author_list': author_list})


