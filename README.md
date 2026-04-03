# edit-metadata
 Edit Metadata


## Project Overview

EditMetadata is a web utility designed for modifying image metadata. The application allows users to upload an image, specify a date, time, and geographic coordinates in degrees, minutes, and seconds (DMS) format, and embed this information into the image metadata.

Additionally, the tool applies a watermark containing the specified metadata values in the lower-left corner of the image and returns the processed image for download.


## Installation

The project is deployed using Docker.

### Prerequisites

- Docker
- Docker Compose

### Setup Instructions

##### 1. Clone the repository

    git clone https://github.com/andreibaliyevich/edit-metadata.git

##### 2. Navigate to the project directory

    cd edit-metadata

##### 3. Create a media directory inside the src folder

    mkdir src/media

##### 4. Create a static directory and add required static files

    mkdir src/static

Place the following files in the static directory inside the src folder:

- favicon.ico
- arialmt.ttf (font file)

> **Note:**
> The `arialmt.ttf` font is required to ensure consistent rendering of the watermark text across different operating systems and environments.
> Without explicitly specifying the font file, text rendering may vary or fail due to missing system fonts inside the Docker container.

##### 5. Build Docker images

    docker compose build

##### 6. Start the service

    docker compose up


## License

This project is licensed under the
[GNU Affero General Public License version 3](https://www.gnu.org/licenses/agpl-3.0.html)
