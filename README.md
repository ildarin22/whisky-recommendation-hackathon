# whisky bottle training

For a Microsoft hackathon, our project was a whiskey recommendation engine with two parts:
* Bottle/Distillery identification
* "Would I like this" bottle/distillery

For this project, we used a number of [Azure Cognitive Services](https://azure.microsoft.com/en-us/services/cognitive-services/), such as:
* [Bing Image Search](https://azure.microsoft.com/en-us/services/cognitive-services/bing-web-search-api/)
* [Custom Vision Service](https://azure.microsoft.com/en-us/services/cognitive-services/custom-vision-service/)

## Source data

Kaggle has a great set of available datasets, so we used this one which has the distillery and a few characteristics of the whiskys.

https://www.kaggle.com/koki25ando/scotch-whisky-dataset/data

## Bottle/Distillery identification

Since our dataset was larger than we wanted to manually train, I created a script to loop through each line in the CSV data above to create a tag in Azure's Custom Vision Service for each distillery.

I then used another script to loop through each tag it found and use Bing's Image Search API and collect the top 10 images that match and insert them as training data for that distillery.

## Cognitive Service API's

Using [Custom Vision](https://customvision.ai) API's, we ingested images found from the Bing Image Search for training data.

NOTE:  I did not use the Python modules, because I found out about them too late.  
https://docs.microsoft.com/en-us/azure/cognitive-services/custom-vision-service/python-tutorial

## Recommendation

The recommendation engine was built with the following information:
* Input:
  * One Scotch - The bottle scanned, as indicated from the Custom Vision API result
  * Two Scotches - Other scotches preferred by the user 
* Output:
  * Score - Percentage that the identified scotch matches the other scotches preferred
* Assumption:
  * Evaluating each attribute from the list of scotches provided:
    * If two scotches have similar values (e.g. both have 0 for smokey), we assume they really want that attribute
    * If two scotches have disparate values (e.g. one has 0 for smokey, and the other has 4), we assume they don't care about that value at all
    * If two scothes have close value (e.g. 1 and 3 for smokey), then we assume they mildly care.
