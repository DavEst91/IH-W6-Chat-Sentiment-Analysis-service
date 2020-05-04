# IH-W6-Chat-Sentiment-Analysis-service

Wellcome to the Shakespeare Sentiment Analysis API Chat!.

![](https://images.unsplash.com/photo-1514306191717-452ec28c7814?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80)

We have been commisioned with creating an sentyment analysis chat using the next tools: Flask for the API creation, NLTK for sentiment analysis, recommender systems, and deployment of the API in Heroku

We have also used MongoDB Atlas as in cloude service for our database.

We've feeded our API with sentences from Shakespeare plays provided in [Kaggle](https://www.kaggle.com/kingburrito666/shakespeare-plays).

The next endpoints are provided:

### User endpoints

* User creation
```/user/create?username=<username>```
* Recommending similar users
```/user/<username>/recommend```

### Chat endpoints

* Create chat
```/chat/create?conversation=conversation_name```

* Add user to chat
```/chat/<conversation>/adduser?username=<username>```

* Add message to chat
```/chat/<conversation_name>/addmessage?username=<username>&message=<messagewithspacesreplacedwith%20>```

* List messages of a chat
```/chat/<conversation_name>/list```

* Analyse sentiments from a chat
```/chat/<chat_id>/sentiment```

The app is actually deployed in https://davestchat.herokuapp.com/
