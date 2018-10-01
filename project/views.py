# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from requests import auth

from project.forms import ProjectForm
from project.models import Project


@login_required(login_url='/login/')
def project_new(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = Project()
            project.author = request.user
            project.first_name = form.cleaned_data['first_name']
            project.last_name = form.cleaned_data['last_name']
            project.email = form.cleaned_data['email']
            project.project_name = form.cleaned_data['project_name']
            project.project_description = form.cleaned_data['project_description']
            project.project_notes = form.cleaned_data['project_notes']
            project.published_date = timezone.now()
            project.lang_choices = form.cleaned_data['select_lang']
            project.save()
            return redirect('projects')
    else:
        form = ProjectForm()
    return render(request, 'blog/project_new.html', {'form': form})


@login_required(login_url='/login/')
def project_details(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'blog/project_detail.html', {'project': project})


@login_required(login_url='/login/')
def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    form = ProjectForm(request.POST or None,
                       initial={'first_name': project.first_name, 'last_name': project.last_name,
                                'email': project.email,
                                'project_name': project.project_name,
                                'project_description': project.project_description,
                                'project_notes': project.project_notes, 'select_langs': project.select_langs,
                                }
                       )

    return render(request, 'blog/project_new.html', {'form': form})


@login_required(login_url='/login/')
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.delete()
    return redirect('projects')


@login_required(login_url='/login/')
def all_projects(request, ):
    project_list = Project.objects.filter(author=request.user)
    query = request.GET.get('q')
    if query:
        project_list = project_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct()

    page = request.GET.get('page', 1)

    paginator = Paginator(project_list, 1)
    try:
        project_list = paginator.page(page)
    except PageNotAnInteger:
        project_list = paginator.page(1)
    except EmptyPage:
        project_list = paginator.page(paginator.num_pages)

    return render(request, "blog/project_detail.html", {'projects': project_list})

