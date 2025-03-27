# M&G Q-Gen: Meet & Greet Question Generator

This application streamlines the Meet & Greet process by automatically generating insightful interview questions based on a candidate's CV/resume. Leveraging the power of Google Cloud's Gemini generative AI model, it extracts key information from the provided PDF and formulates questions tailored to the candidate's experience and the specified domain.

## Core Components:

1. **`main.py`**: The main application file that orchestrates the Gradio interface and interacts with other components. It handles user input (CV upload and domain selection) and displays the generated questions.

2. **`question_generator.py`**: Contains the core logic for question generation.  It uses the `PdfExtractor` to get candidate information and the `GeminiModel` to generate questions based on predefined prompts.  The `QuestionGenerator` class orchestrates the process based on the specified domain. **`pdf_extractor`** extracts relevant information from the uploaded PDF using the Gemini model with a JSON output schema.  It handles potential errors like file not found, permission errors, and other OS errors during file access.

3. **`gemini.py`**:  Provides a wrapper for interacting with Google Cloud's Gemini model. The `GeminiConfig` dataclass manages parameters like temperature, top_p, top_k, and system instructions for the model.

4. **`prompts.py`**: Stores the prompts used to guide the Gemini model for both information extraction and question generation.  These prompts are tailored for different question categories (experience, tech stack, industry, data analysis, Generative AI, and consulting).

5. **`gemini_schema.py`**: Defines the JSON schema for the output of the PDF extraction process. This ensures consistent and structured data extraction.

6. **`logging_utils.py`**: Sets up a basic logger for debugging and informational messages.

7. **`requirements.txt`**: Lists the required Python packages for the application.

8. **`Dockerfile`**: Defines the Docker image for containerizing the application, based on `python:3.12-slim`.  It copies the application code, installs dependencies, and exposes port 8080.

9.  **`build_deploy.sh`**: A shell script to build and deploy the Docker image to Google Cloud Run. It takes the image name, region, repository, and project ID as arguments.

10. **`pyproject.toml`**: Manages project metadata, dependencies, and code style configurations. It also configures tools like `black`, `isort`, and `pylint`.

11. **`.pre-commit-config.yaml`**: Configures pre-commit hooks to enforce code quality and consistency.


## Data Store:

This directory contains files related to setting up and using a Vertex AI Search data store for storing and retrieving interview questions (TODO: for grounding the question generation, include as part of the main application).

1. **`commands.sh`**: Contains shell commands for creating a Cloud Storage bucket, and uploading a PDF file to the. This PDF contains the interview questions dataset. In the future there could be questions by specialization.

2. **`get_questions.py`**: This script retrieves answers from the Vertex AI Search engine based on a given query. It demonstrates how to interact with the Search API.

3. **`create_ds.py`**: This script creates a Vertex AI Datastore and imports documents from a specified GCS URI.  It uses helper functions from a `utils.py`  to interact with the Vertex AI API.  This script sets up the necessary infrastructure for the Search functionality.



## Code Style and Quality Enforcement:

This project utilizes several tools to maintain code quality and consistency. These tools are configured in `pyproject.toml` and `.pre-commit-config.yaml`:

**Pre-commit Hooks (`.pre-commit-config.yaml`):**

- `check-merge-conflict`, `trailing-whitespace`, `end-of-file-fixer`, `check-toml`, `check-yaml`, `check-symlinks`, `check-added-large-files`, `requirements-txt-fixer`, `forbid-new-submodules`, `no-commit-to-branch`, `detect-private-key`, `mypy`, `black`, `pylint`, `isort`: These hooks ensure code style, prevent common errors, and enforce best practices.  See the `.pre-commit-config.yaml` file for details on each hook.

**`pyproject.toml` Configuration:**

- **`[tool.black]`**: Configures Black for code formatting (line length 119).
- **`[tool.isort]`**: Configures isort for import sorting.
- **`[tool.pylint]`**: Configures Pylint, including disabling specific checks (e.g., line length, trailing whitespace) that are handled by other tools.  It also limits the maximum number of attributes per class to 10.


## Containerization and Deployment:

The application is containerized using Docker and deployed to Google Cloud Run.

### Prerequisites for Deployment:

Before deploying to Google Cloud Run, ensure the following prerequisites are met:

1.  **Google Cloud Project:** You must have a Google Cloud project set up.
2.  **Artifact Registry:**
    *   Create a Docker repository in Google Cloud Artifact Registry to store your Docker images.
    *   You can create a repository using the gcloud CLI or the Google Cloud Console.
    *   Example using gcloud CLI:
        ```bash
        gcloud artifacts repositories create <REPOSITORY_NAME> \
        --repository-format=docker \
        --location=<REGION> \
        --description="Docker repository for M&G Q-Gen"
        ```
        *   Replace `<REPOSITORY_NAME>` with your desired repository name (e.g., `mg-q-gen-repo`).
        *   Replace `<REGION>` with the region where you want to create the repository (e.g., `us-central1`).
3.  **Cloud Build API:** Enable the Cloud Build API in your Google Cloud project.
4. **Cloud Run API:** Enable the Cloud Run API in your Google Cloud project.

### Setting up Cloud Build Trigger:

To automate the deployment process, you need to create a Cloud Build trigger that will automatically build and deploy your application whenever changes are pushed to the main branch.

1.  **Create a Trigger:**
    *   Go to the Cloud Build Triggers page in the Google Cloud Console.
    *   Click "Create Trigger."
    *   Configure the trigger as follows:
        *   **Name:** Give your trigger a descriptive name (e.g., `deploy-to-cloud-run`).
        *   **Region:** Select the region where you want to run the build.
        *   **Event:** Select "Push to a branch."
        *   **Source:** Choose your repository and select the `main` branch.
        *   **Configuration:** Select "Cloud Build configuration file (yaml)" and specify the location of your `cloudbuild.yaml` file (e.g., `/cloudbuild.yaml`).
        * **Substitutions:** Add the following substitution variables:
            * `_GCR_HOSTNAME`: The hostname of your artifact registry, for example: `us-central1-docker.pkg.dev`
            * `_PROJECT`: Your project ID.
            * `_REPOSITORY`: The name of your artifact registry repository.
            * `_IMAGE_NAME`: The name of the image.
    *   Click "Create."

2.  **Environment Variables:**
    *   The `cloudbuild.yaml` file uses substitution variables (e.g., `${_GCR_HOSTNAME}`, `${_PROJECT}`, `${_REPOSITORY}`, `${_IMAGE_NAME}`).
    *   These variables are defined in the trigger configuration.
    *   Ensure that the values you set in the trigger match your project's configuration.

### Manual Deployment (`build_deploy.sh`):

-   The `build_deploy.sh` script builds the Docker image and pushes it to Google Container Registry.
-   It then deploys the image to Cloud Run, specifying the region, port, and allowing unauthenticated access.
-   The `cloudbuild.yaml` file is used by the Cloud Build trigger to define the build and deployment steps.


## Running Locally:

1. Ensure you have Docker installed.
2. Navigate to the project root directory (the directory containing this README).
3. Build the Docker image, specifying the Dockerfile path: `docker build -t mg-q-gen -f src/app/Dockerfile .`
4. Run the Docker container: `docker run -p 8080:8080 mg-q-gen`
5. Access the application in your browser at `http://localhost:8080`.

## Contributing:

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature: `git checkout -b feature/your-feature-name`
3. Set up pre-commit hooks: `pre-commit install`
4. Make your changes and commit them: `git commit -m "Your commit message"` (pre-commit will run automatically on commit)
5. Push your branch: `git push origin feature/your-feature-name`
6. Create a pull request against the `development` branch.
