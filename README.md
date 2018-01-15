# URL_Shortener
Django app on Django development server to short your long URLs


##Prerequisites

You may need Docker and Docker-compose installed


## Running

To run the project for first time: go to project folder in your shell and run

```
docker-compose up --build
```
After built you will have running app on http://localhost:8000

## What this app can do
  - Create short version of long url by yourself or random generate it, when you access short url it will redirect you to original URL
  - Count amount of short url usage
  - Manage created URLs (CRUD abilities)
  - Remove URL from db on 14th day after its creation
  - Store text from the first html-tag(p, span, h1-h6, td) on page

  also it has Creation API created with DjangoRestFramework (to access it go to  http://localhost:8000/api/create)

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds
