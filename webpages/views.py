from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from accounts.models import Profile
from webpages.models import Page
from rest_framework.decorators import api_view
from rest_framework import status
from webpages.serializers import PageSerializer


@api_view(["POST"])
def save_page(request, email):
    # Verify the email exists in the accounts model
    profile = get_object_or_404(Profile, email=email)

    if request.method == 'POST':
        # Extract the title, HTML, and CSS content from the request
        title = request.data.get('title')
        html_content = request.data.get('html_content')
        css_content = request.data.get('css_content')

        if not title:
            return Response({'message': 'Title is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new instance in the webpages model, linking it with the email
        page = Page.objects.create(title=title, html_content=html_content, css_content=css_content, user_email=profile)

        # Return a JSON response with the page ID and success message
        return Response({'page_id': page.id, 'message': 'Page saved successfully.'}, status=status.HTTP_200_OK)

    # Return an error message for unsupported request methods
    return Response({'message': 'Invalid request method.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def view_all_pages(request, email):
    try:
        profile = Profile.objects.get(email=email)
    except Profile.DoesNotExist:
        return Response({"error": "Invalid email"}, status=status.HTTP_400_BAD_REQUEST)

    pages = Page.objects.filter(user_email=profile)
    serializer = PageSerializer(pages, many=True)
    data = {
        'pages': serializer.data
    }
    return Response(data, status=status.HTTP_200_OK)


@api_view(["DELETE"])
def delete_page(request, id):
    page = get_object_or_404(Page, id=id)
    if request.method == "DELETE":
        page.delete()
        return Response({"detail": "Page deleted"}, status=status.HTTP_200_OK)

@api_view(["PUT"])
def modify_page(request, id):
    page = get_object_or_404(Page, id=id)

    if request.method == "PUT":
        page.title = request.data.get('title', page.title)
        page.html_content = request.data.get('html_content', page.html_content)
        page.css_content = request.data.get('css_content', page.css_content)
        page.save()
        return Response({"detail": "Page modified"}, status=status.HTTP_200_OK)
