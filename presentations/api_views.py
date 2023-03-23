from django.http import JsonResponse
from common.json import ModelEncoder
from .models import Presentation
from events.api_views import ConferenceDetailEncoder, Conference
from django.views.decorators.http import require_http_methods
import json


class PresentationDetailEncoder(ModelEncoder):
    model = Presentation
    properties = [
        "presenter_name",
        "company_name",
        "presenter_email",
        "title",
        "synopsis",
        "created",
        "conference"
    ]
    encoders = {
        "conference": ConferenceDetailEncoder()
    }


class PresentationListEncoder(ModelEncoder):
    model = Presentation
    properties = [
        "title",
    ]

    def get_extra_data(self, o):
        return {"status": o.status.name}


@require_http_methods(["GET", "POST"])
def api_list_presentations(request, conference_id):
    if request.method == "GET":
        presentations = Presentation.objects.all()
        return JsonResponse(
            {"presentations": presentations},
            encoder=PresentationListEncoder,
        )
    else:
        content = json.loads(request.body)

        try:
            conference = Conference.objects.get(id=conference_id)
            content["conference"] = conference
        except Conference.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid conference id"},
                status=400
            )

        presentations = Presentation.create(**content)
        return JsonResponse(
            presentations,
            encoder=PresentationListEncoder,
            safe=False,
        )


@require_http_methods(["DELETE", "GET", "PUT"])
def api_show_presentation(request, id):
    if request.method == "GET":
        presentation = Presentation.objects.get(id=id)
        return JsonResponse(
            presentation,
            encoder=PresentationDetailEncoder,
            safe=False,
        )
    elif request.method == "DELETE":
        count, _ = Presentation.objects.filter(id=id).delete()
        return JsonResponse({"deleted": count > 0})
    else:
        content = json.loads(request.body)
        try:
            if "conference" in content:
                conference = Conference.objects.get(id=id)
                content["conference"] = conference
        except Conference.DoesNotExist:
            return JsonResponse(
                {"message": "Conference"},
                status=400,
            )
        Presentation.objects.filter(id=id).update(**content)
        location = Presentation.objects.get(id=id)
        return JsonResponse(
            location,
            encoder=PresentationDetailEncoder,
            safe=False,
        )
