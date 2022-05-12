import pytest
from model_bakery import baker
from rest_framework.test import APIClient

from students.models import Course, Student


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_get_first_course(client, course_factory):
    courses = course_factory(_quantity=10)
    first_course = Course.objects.first()
    response = client.get(f'/courses/{courses[0].id}/')
    assert response.status_code == 200
    assert response.data['id'] == first_course.id
    assert response.data['name'] == first_course.name


@pytest.mark.django_db
def test_get_courses(client, course_factory):
    course_factory(_quantity=20)
    all_courses = Course.objects.all()
    response = client.get('/courses/')
    assert response.status_code == 200
    assert len(response.data) == len(all_courses)


@pytest.mark.django_db
def test_filter_id(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get('/courses/', {"id": courses[0].id})
    assert response.status_code == 200
    for item in response.data:
        assert item['id'] == courses[0].id


@pytest.mark.django_db
def test_filter_name(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get('/courses/', {"name": courses[0].name})
    assert response.status_code == 200
    for item in response.data:
        assert item['name'] == courses[0].name


@pytest.mark.django_db
def test_create_course(client):
    count = Course.objects.count()
    response = client.post('/courses/', {'name': 'First course', 'students': []})
    assert response.status_code == 201
    assert Course.objects.count() == count+1


@pytest.mark.django_db
def test_update_course(client, course_factory):
    courses = course_factory(_quantity=5)
    response = client.patch(f'/courses/{courses[0].id}/', {'name': 'Updated name'})
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_course(client,course_factory):
    courses = course_factory(_quantity=5)
    count = Course.objects.count()
    response = client.delete(f'/courses/{courses[0].id}/')
    assert response.status_code == 204
    assert Course.objects.count() == count-1


