# YT Blog Generator

This is a Django-based backend application that provides APIs for generating blogs using AI tools. Follow these instructions to clone, set up, and run the project.

## Prerequisites

Ensure you have the following installed on your system:

- Python (>= 3.8)
- PostgreSQL
- Git

---

## Setup Instructions

### 1. Clone the Repository

```bash
$ git clone <repository-url>
$ cd YT_blog_generator
```

### 2. Configure Environment Variables

1. Create a `.env` file in the `Backend/ai_blog_app` directory.
2. Add the following environment variables:

```env
DATABASE_URL=postgresql://<username>:<password>@<host>/<database_name>
AAI_SETTINGS_API_KEY="<your-api-key>"
OPEN_AI_KEY="<your-openai-key>"
```

Replace `<username>`, `<password>`, `<host>`, `<database_name>`, and keys with your actual values.

### 3. Set Up the Database

1. Apply the migrations:

```bash
$ python3 manage.py makemigrations
$ python3 manage.py migrate
```

### 4. Create a Superuser

To access the Django admin panel, create a superuser:

```bash
$ python3 manage.py createsuperuser
```

Follow the prompts to set up a username and password.

### 5. Run the Server

```bash
$ python3 manage.py runserver
```

The application will be accessible at `http://127.0.0.1:8000/`.

---

## Project Structure

```plaintext
YT_blog_generator/
├── Backend/
│   ├── ai_blog_app/
│   │   ├── migrations/
│   │   ├── templates/         # HTML templates
│   │   ├── settings.py        # Django settings
│   │   ├── urls.py            # URL routing
│   │   ├── views.py           # View functions
│   ├── blog_generator/        # Blog app
├── Frontend/                  # (Optional, for UI or frontend-related files)
├── .env                       # Environment variables
├── manage.py                  # Django's command-line utility
└── README.md                  # Project instructions
```

---

## Usage

1. Navigate to the following endpoints in your browser or API client:

   - `/signup`: User signup page.
   - `/login`: User login page.
   - `/generate-blog`: API for blog generation.

2. Access the Django admin panel at `http://127.0.0.1:8000/admin` using your superuser credentials.

---

## Troubleshooting

### Common Issues:

- **Database Connection Errors:**
  Ensure your PostgreSQL server is running and the credentials in `.env` are correct.

- **Missing Environment Variables:**
  Double-check the `.env` file for missing or incorrect values.

---

## Contributing

Feel free to submit issues or create pull requests. Contributions are welcome!

---

## License

This project is licensed under the MIT License.
