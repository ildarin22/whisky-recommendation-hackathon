# whisky bottle training

For a Microsoft hackathon, our project was a whiskey recommendation engine with two parts:
* Bottle/Distillery identification
* "Would I like this" bottle/distillery

For this project, we used a number of [Azure Cognitive Services](https://azure.microsoft.com/en-us/services/cognitive-services/), such as:
* (Bing Image Search)[https://azure.microsoft.com/en-us/services/cognitive-services/bing-web-search-api/]
* (Custom Vision Service)[https://azure.microsoft.com/en-us/services/cognitive-services/custom-vision-service/]

## Source data

Kaggle has a great set of available datasets, so we used this one which has the distillery and a few characteristics of the whiskys.

https://www.kaggle.com/koki25ando/scotch-whisky-dataset/data

## Bottle/Distillery identification

Since our dataset was larger than we wanted to manually train, I created a script to loop through each line in the CSV data above to create a tag in Azure's Custom Vision Service for each distillery.

I then used another script to loop through each tag it found and use Bing's Image Search API and collect the top 10 images that match and insert them as training data for that distillery.
