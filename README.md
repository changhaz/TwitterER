TwitterER: 
=========
Opinion Mining based on comparison



<h3>What is TwitterER?</h3>

TwitterER originates from the NLP project ‘Opinion Mining based on Comparison’, which is the final project for course 'CSCI 544 - Applied Natural Language Processing' instructed by Zornitsa Kozareva in USC. When given two query terms (each of which could be the name of a product, a person, a company, etc), the goal is to compare and find out which one is more favored by people.

<h3>Where does data come from? What is inside the system?</h3>

TwitterER deals with real-time data from Twitter, and get results of comparison with the help of Machine Learning and Natural Language Processing. 

TwitterER = Twitter (source of data) + ER (which means comparison, like bettER and fastER) 
TwitterER = NLP + ML 

<h3>What kind of object could I search?</h3>

Basically all the pairs of competing objects or persons could be a good candidate for this NLP analysis. Here are just some suggestions, further usage is for you to explore. 

For people who like to purchase a new mobile phone, and hesitate between two most popular models: iPhone and Galaxy, you could now easily hear what other people prefers and their unique reasons by searching 'iphone' and 'galaxy' in TwitterER. 

For NBA fans, before each round of match, it is your habits to see other people's comments or prediction. Now, you could get plenties of information about the East Final Play-off just by seaching for 'Heat' and 'Pacer'. 

For journalists who want to see public's preference between two candidates in the campaign, you could now search the name of two candidates in TwitterER. It will show you the approval ratings quickly and precisely. 

For companys who love to do market researches, now your job is as easy as typing in the name of your product and its opponent, then wait for TwitterER to give you a full analysis. As you can see, social network is the place consumers like to comment about your products. 
... 

<h3>Why is it interesting and who would use it when solved?</h3>

Most of the existing researches and applications on sentiment analysis mainly focus on one certain object. For example, existing systems like ‘Sentiment140’ merely output the sentiment over one certain product or brand. The positive-negative percent given by ‘Sentiment140’ could be helpful to some extent for consumers who want to research the sentiment of products before purchase. Unfortunately, its help could not be that much. This is because when consumers are making decisions before purchase, there’s one important step involved but ignored by these existing systems. This step is comparison. 

Before their purchase of certain product, consumers always want to know: is there any substitute for it? It is the first sub-problem we will solve in our project. This problem worth our attention because when we check product reviews, a 4-star rating or praises in comment will not directly lead us to make our decision. If there are some similar products from other brands, also with 4-star rating, then consumers still don’t know which one to choose. Therefore, finding substitutes is very important. 

When consumers already found some substitute products, they start to compare. Consumers tend to compare the price, function, and more importantly, reputation. While price and function could be easily searched, quantized and compared, reputation of two products is still hard to compare in an efficient way. So we make it as our second sub-problem. Our goal here is to build a new NLP system using sentimental analysis based on comparison. 

These two problems solved, consumers will have a new experience in e-commerce. For example, one year later, your iPhone 5 will be too old so you want to have a new mobile phone. Unfortunately you are an NLP specialist but know little about electrical devices. What could come to your mind is no more than the latest iPhone: iPhone 25. So you just input iPhone 25 in our system. You get the name of two other currently most popular mobile phones: Samsung Galaxy s 300 and Nokia 0000. Maybe you are not interested in Samsung’s face size screen anymore, so you click Nokia 0000 and see the comparison of reputation between iPhone and 0000. Our system will give the percentage of the people who prefer iPhone, the percentage of people who choose Nokia and those who love them both. Plus, in the following small blocks, people’s detail comments on these two products are given into these three groups respectively. All these make it easy for you to find out what features makes one model more popular than the other. Now it’s up to you to choose which one to purchase… 

Of course, the functionality of the system is not restricted to consumer’s view. It also help companies to monitor the public sentiment of their brands, and more importantly, public preference of their brands when compared to their competitors. 

<h3>Contact us</h3>

TwitterER system is developed by Changhai Zheng and Yunqing Cao. Web demo is developed by Changhai Zheng. 

If you have any questions or advice, please contact zch1017 (at) gmail (dot) com. 



