# Quote Finder
A small demo flask web app that finds a quote on any given genre.

## Dataset
The quotes are pulled from a CSV file obtained from [TheWebMiner](https://thewebminer.com/buy-famous-quotes-database) containing around 76,000 quotes across 117 genres, by over 11,000 authors.

## A quote lookup? Where's the AI?
Since there are only 117 genres in the quote library, if the user asks for a theme that doesn't exist as a label by itself the app will attempt to find the closest match. Sometimes it's good, sometimes not so good!

The closest match is identified by translating the requested genre and all existing genre labels into multi-dimensional vectors and locating the closest using a measure called cosine distance. The vectors were learned from text samples such that similar words have similar vector representations.

## Try the app
[http://quote-finder.azurewebsites.net](http://quote-finder.azurewebsites.net)

## Author
Aleem Juma
