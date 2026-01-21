from __future__ import annotations

from pathlib import Path

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from expansao360.application.use_cases import register_location
from expansao360.infrastructure.file_repositories import FileLocationRepository

from .forms import LocationForm


def location_create(request: HttpRequest) -> HttpResponse:
    message = None
    error = None

    if request.method == "POST":
        form = LocationForm(request.POST)
        if form.is_valid():
            try:
                state_path = Path(".expansao360-state.json").resolve()
                repo = FileLocationRepository(state_path)
                loc = register_location(
                    location_id=form.cleaned_data["location_id"],
                    name=form.cleaned_data["name"],
                    repository=repo,
                )
                message = f"Location criada: {loc.id} — {loc.name}"
                form = LocationForm()
            except ValueError as e:
                error = str(e)
    else:
        form = LocationForm()

    return render(
        request,
        "location_create.html",
        {"form": form, "message": message, "error": error},
    )
