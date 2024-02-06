from pydantic import BaseModel, ConfigDict


class Course(BaseModel):
    title: str
    description: str
    author: str
    category: str
    difficulty: str
    status: str

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'title': 'Введение в Python',
                    'description': 'Изучите основы Python.',
                    'author': 'Джейн До',
                    'category': 'Программирование',
                    'difficulty': 'Начальный',
                    'status': 'Активный',
                }
            ]
        }
    }


class CourseCreate(Course):
    pass


class CourseRead(Course):
    id: int

    model_config = ConfigDict(from_attributes=True)
