
from django.shortcuts import render, redirect
import markdown2
from . import util
import random

def index(request):
    entries = util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })



def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": f"The page '{title}' was not found."
        })
    html_content = markdown2.markdown(content)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html_content
    })



def search(request):
    query = request.GET.get("q", "")
    if util.get_entry(query):
        return redirect('entry', title=query)
    results = [entry for entry in util.list_entries() if query.lower() in entry.lower()]
    return render(request, "encyclopedia/search.html", {
        "results": results,
        "query": query
    })

def new_page(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        if util.get_entry(title):
            return render(request, "encyclopedia/error.html", {
                "message": f"An entry with the title '{title}' already exists."
            })
        util.save_entry(title, content)
        return redirect('entry', title=title)
    return render(request, "encyclopedia/new.html")



def edit(request, title):
    content = util.get_entry(title)
    if request.method == "POST":
        updated_content = request.POST["content"]
        util.save_entry(title, updated_content)
        return redirect('entry', title=title)
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })

def random_page(request):
    entries = util.list_entries()
    title = random.choice(entries)
    return redirect('entry', title=title)


def category(request, category_name):
    entries = util.list_entries()
    results = [entry for entry in entries if category_name.lower() in entry.lower()]
    return render(request, "encyclopedia/category.html", {
        "category_name": category_name,
        "results": results
    })
