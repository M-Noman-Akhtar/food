from django.shortcuts import render
from .models import Calorie
from textblob import TextBlob
import psycopg2 as pg2
import numpy as np
import pandas as pd
from tabulate import tabulate
from textblob import classifiers
from textblob.classifiers import NaiveBayesClassifier
import matplotlib.pyplot as plt

def home(request):
    return render(request, 'home.html');

def Main(request):
    return render(request, 'Main.html');

def Calculate_Calorie(request):
    return render(request, 'Calculate_Calorie.html');

def result(request):
    cal = Calorie()
    cal.name = str(request.POST['name'])
    cal.activity_level = str(request.POST['activity_level'])
    cal.weight = int(request.POST['weight'])
    cal.aim = str(request.POST['aim'])
    cal.food = str(request.POST['food'])
    cal.gender = str(request.POST['gender'])
    cal.age = int(request.POST['age'])
    cal.feet = float(request.POST['feet'])
    cal.inches = float(request.POST['inches'])
    cal.height = (cal.feet*30.48) + (cal.inches*2.54)
    if (cal.gender=='male'):
        bmr = 66.5 + (13.75 * cal.weight) + (5.003 * cal.height) + (6.755 * cal.age)
        if(cal.activity_level=='little'):
            cal.c = bmr * 1.2
        elif(cal.activity_level=='light'):
            cal.c = bmr * 1.375
        elif(cal.activity_level=='medium'):
            cal.c = bmr * 1.55
        elif(cal.activity_level=='high'):
            cal.c = bmr * 1.725
        else:
            cal.c = bmr * 1.9
    elif (cal.gender=='female'):
        bmr = 655.1 + (9.563 * cal.weight) + (1.850 * cal.height) + (4.676 * cal.age)
        if(cal.activity_level=='little'):
            cal.c = bmr * 1.2
        elif(cal.activity_level=='light'):
            cal.c = bmr * 1.375
        elif(cal.activity_level=='medium'):
            cal.c = bmr * 1.55
        elif(cal.activity_level=='high'):
            cal.c = bmr * 1.725
        else:
            cal.c = bmr * 1.9
    cal.c=round(cal.c, 2)
    global a,c,n,i
    a = cal.aim
    c = cal.c
    n = cal.food
    return render(request, "result.html",{'cal':cal});

def load(request):
    data = Calorie()
    aim = a
    cal = c
    rec = n.lower()
    connect = pg2.connect(database='food', user='postgres', password='0786')
    query = "SELECT * FROM raw_recipe"
    df = pd.read_sql(query, con=connect)
    df = pd.DataFrame(df, columns=['id', 'name', 'calories', 'ingredients'])
    if (aim == 'lose'):
        df = df[(df['calories'] <= cal) & (df.name.str.contains(rec))]
    if (aim == 'gain'):
        df = df[(df['calories'] >= cal) & (df.name.str.contains(rec))]
    if (aim == 'maintain'):
        df = df[(df['calories'] <= cal + 150) & (df['calories'] >= cal - 150) & (df.name.str.contains(rec))]
    df = df.head(30)
    # df = df.to_numpy()
    headers = ["Id", "Name", "Calories", "Ingredients"]
    table = tabulate(df, headers, tablefmt="fancy_grid", showindex=False)
    data.list = table
    return render(request, "load.html",{'data':data});

def processing(request):
    pre = Calorie()
    pre.desire = request.POST['desire']
    i = pre.desire
    id = int(i)
    global des
    des = id
    connect = pg2.connect(database='food', user='postgres', password='0786')
    # query = 'SELECT * FROM public.reviews'    //if we want to select and search through all data of user's interactions.
    query = 'SELECT * FROM public.interactions'
    df = pd.read_sql(query, con=connect)
    df = pd.DataFrame(df, columns=['recipe_id', 'rating', 'review'])
    df = df[df.recipe_id == id]
    df = df.head(10)
    headers = ["recipe_id", "rating", "review"]
    table = tabulate(df, headers, tablefmt="fancy_grid", showindex=False)
    pre.pre = table
    return render(request, "processing.html",{'pre':pre});

def sentiment(request):
    sent = Calorie()
    sent.desire = des
    id = int(sent.desire)
    connect = pg2.connect(database='food', user='postgres', password='0786')
    # query = 'SELECT * FROM public.reviews'    //if we want to select and search through all data of user's interactions.
    query = 'SELECT * FROM public.interactions'
    df = pd.read_sql(query, con=connect)
    df = pd.DataFrame(df, columns=['recipe_id', 'review'])
    df = df[df.recipe_id == id]
    df = df.head(10)
    df = df.to_string(index=False)
    blob = TextBlob(df).sentiment
    sent.sent = blob
    train = [
        ('Delicious!!! Great flavour and easy to prepare - this was a hit with the family. My only problem with the recipe is that you didnot state a temperature for the oven - I baked at 180C for about 40 minutes. Thanks for a great meal and good luck!!!', 'pos'),
        ('Excellent dish.  The topping is wonderfully rich and really makes the dish!', 'pos'),
        ('WOW!!! If I can please everyone at my table it is got to be GOOD.  This chicken had a wonderful flavor and was so simple to prepare.  Thank you.', 'pos'),
        ('I hate to be the bad apple in the bunch but my entire family was very disappointed. We thought the flavor was too bland. I ended up heating some soy/ginger sauce up and pouring it over it so that we could eat it. Very disappointed.', 'neg'),
        ('I am tired of this stuff.', 'neg'),
        ("I'm sorry, but I followed the directions exactly. The chicken was extremely tender, but the taste was worse than bland. I am using the leftovers in a casserole tonight. I will use the general idea again, but put seasoning on the chicken first. Thanks for sharing your recipe; maybe it's just a difference of taste!", 'neg'),
        ("Neither my kids or my husband were dazzled by this.  I made a pot pie out of the leftovers but the initial chicken was not a winner", 'neg'),
        ("We were expecting a chicken with more of a jerk heat but were not disappointed. We like our jerked chicken with skin so I did not use boneless skinless chicken. The topping was very good and I would suggest doubling it!!! yummy!!! Good luck Chef!", 'pos'),
        ("Delicious!!  Made to the recipe apart from cutting my chicken into largish chunks. Great flavour and easy to prepare - this was a hit with the family. My only problem with the recipe is that you didn't state a temperature for the oven - I baked at 180C for about 40 minutes. Thanks for a great meal and good luck!!!", 'pos'),
        ("We loved this chicken, even the picky daughter. The jerk rub did just as you said and filled the house with lovely smells! For the topping I used 3 cloves of garlic, (we love garlic!), and 1 jalapeno. I didn't need to let the sauce thicken on the stove. It thickened nicely in the oven. The chicken baked for 45 minutes, (the chicken breasts were large), and came out moist and perfectly cooked. I will be making up a quantity of the jerk rub for future use! Great recipe! ", 'pos'),
        ("Ok last night I decided I wanted chicken so I came to zaar to seek out one of the RSC recipes and I found a true winner. I did not have the habanero pepper but it still tasted nummy!! You cannot believe the wonderful smell that fills the house. Why have plain chicken again. The list of ingredients seems intimidating but it really not a huge task to add. Someone really put their thinking caps on for this one. I love it !!!", 'pos'),
        ("This recipe is now the fav chicken dish in our house. My husband was very tired of the same old, so I decided to try something new. I only let the rub mix set for one hour, but next time I will let it sit longer so the flavor is more intence. And I am not a habanero fan, so I split this in two pans, but I ended up helping my husband and son eat their share. I hope to see more recipes like this. Thanks", 'pos'),
        ("This was very tasty and very spicy! I had to replace chives with parsley and habanero with pickled jalapeno (couldn't get them). Also used chicken thighs instead of breasts. Recipe didn't give a temp. to bake at so I did at 375Ã‚Â°F for 35 minutes. Chicken was nice and moist. Loved the flavors from the seasoning mix. Thanks and good luck in the contest! - Mar 5, 2006 Update: I had some of this in the freezer and wanted to do something a little different with it. I thawed out a serving (a couple thighs worth) and then mixed it with a pkg of cream cheese, a couple Tbsp mayo and 1/2 cup shredded cheddar cheese to make an excellent chicken salad! Thanks again Pamela!", 'pos'),
        ("Very very good! I mixed the spices together and added it to a bag of skineless chicken legs and thighs, and froze it for several weeks.  I pulled it out of the freezer last nigth to thaw in the fridge.  I mixed up the topping just before baking, and added an additional teaspoon of brown sugar to the topping to sweeten it up a little more for my family's liking, and a few dashes of hot pepper sauce in place of the habenero.  I only added the topping to half the chicken (due to the kids).  It baked up so fantastically- the chicken without the topping were flavorful but not too spicy, the ones with the topping were so flavorful and delicious.  What a great recipe- thanks for posting!", 'pos'),
        ("I really liked the flavour in this.  As we can't handle things too hot I cut the cayenne into a 1/4 teaspoon and omitted the habanero pepper and it was perfect.  Lightly spiced without burning the mouth.  We really enjoyed it.  Thanks for sharing!", 'pos'),
        ("It was wonderful spicewise but we used half a cup of serranos for our peppers and it was way too hot - and we know spicey! I will use the serranos again next time but probably a 1/4 cup of them so I can enjoy the other spices.", 'pos'),
        ("This was very good, served it over rice.  I used an unseeded jalapeno instead of the habenero and it was plenty spicy!  Leftover chicken will go into a soup for dinner on Monday night which is something that I do often when we have leftover chicken.  Reviewed for Healthy Choices 2008 ABC Tag Game.", 'pos'),
        ("I made this tonight for supper and we loved it.  The chicken was moist and juicy with the lovely vegetable mixture on top.  I served this with rice and peas and glazed carrots.  Thank you for sharing this recipe with us, its a keeper.", 'pos'),
        ("I expected it to taste like something Jamaican and it really didn't to me. It was not at all  what I expected and it may have been better without the crushed tomatoes.", 'neg'),
        ("This is dish creates the most amazing aroma in the kitchen while it&#039;s baking, and then the most amazing flavors explode in your mouth while eating it. I love serving this over rice and a side salad.  Such a different flavor experience. I usually try not to step too far out of my comfort zone with recipes, but I took a chance on this one and it&#039;s now one of our absolute favorites.", 'pos'),
        ("This is dish creates the most amazing aroma in the kitchen while it&#039;s baking, and then the most amazing flavors explode in your mouth while eating it. I love serving this over rice and a side salad.  Such a different flavor experience. I usually try not to step too far out of my comfort zone with recipes, but I took a chance on this one and it&#039;s now one of our absolute favorites.", 'pos'),
        ("We enjoyed this dish very much. The house smelled terrific during cooking. The only thing I would do, as mentioned in other reviews, is to add seasoning to the chicken.  We served with rice cooked in chicken broth and a green salad.  Very yummy! ", 'pos'),
        ("OMG!  This is DELICIOUS and oh so easy!  I too have the concentrated smoke and used about 2 teaspoons only.  I cooked all day and it was out of this world!  Whole family LOVED it!  THANKS a MILLION! ", 'pos'),
        ("This chicken was fantastic and so easy! I could hardly get the chicken out of the crockpot in one piece. It was incredibly juicy and tender. We had the levtovers for lunch the next day and it was great even a day later. This is a wonderful weekday meal; just add a side of rice and vegetables and it's finished!", 'pos'),
        ("I hate to be the bad apple in the bunch but my entire family was very disappointed. We thought the flavor was too bland. It needed some seasoning or something. I ended up heating some soy/ginger sauce up and pouring it over it so that we could eat it. Very disappointed.   ", 'neg'),
        ("This is absolutely DELISH! This has to be the fastest and easiest recipe ever - cheaper and quicker than fast food! I  bought a whole chicken for $3 and the liquid smoke was 88 cents. This was so tender and juicy, the meat just fell off the bones, and it smells so good. I prepared this exactly as the recipe states. Takes 2 min to prepare and you are done. I'll be making this one a lot - thanks so much!", 'pos'),
        ("Very good chicken.  After reading the previous comments about the bland turnout, I rubbed the entire chicken with lemmon pepper and rotisserie seasoning.  I also halved a lemon and stuck that in the pot as well.  It turned out very moist and tender.  I look forword to all the leftovers we'll have this week!", 'pos'),
        ("O WOW! I couldn't believe it wasn't smokehouse. Soooo Good!! I used a turkey breast; pulled up the skin; mixed minced garlic, sage, sweet basil with a little olive oil. spread that on the breast and pulled skin back into place. Cooked for 8 hours, breast side down.   O WOW again...got rave reviews? ThatBobbyGirl, you're a cooking genius! Thanks for sharing.", 'pos'),
        ("Excellent.  I too added some seasoning salt and pepper and tossed an onion into the bottom of the pot.  I made orzo with the juice and it was just great.  ", 'pos'),
        ("This was really good!  I used an entire bottle of Liquid Smoke and also added some garlic powder and seasoning salt to the chicken. I cooked it for 10 hours. I tried to pick it up out of the pot to place it on a plate to take the meat off and couldn't because the meat fell off the bone, so tender!  This made a great supper for my low carb diet and I can't wait to eat it for lunch tomorrow served over a salad.  Thanks for posting!", 'pos'),
        ("This was one of the easiest recipes that I've tried - the flavor was excellent. The chicken tasted like I'd worked all day. Thanks for sharing.", 'pos'),
        ("I'm sorry, but I followed the directions exactly. The chicken was extremely tender, but the taste was worse than bland. I am using the leftovers in a casserole tonight. I will use the general idea again, but put seasoning on the chicken first. Thanks for sharing your recipe; maybe it's just a difference of taste!", 'neg'),
        ("Neither my kids or my husband were dazzled by this.  I made a pot pie out of the leftovers but the initial chicken was not a winner", 'neg'),
        ("Sorry...we really didn't like this recipe.  It scores points for being easy enough for my husband to throw in the crockpot while I'm at work, but it turned out pretty flavorless and dry.  I didn't look forward to my lunch of leftovers the next day.", 'neg'),
        ("What a unique and creative way to cook an old bird!!  This was marvellous!!  And the defatted sauce made a terrific gravy!  Love these simple but fabulous recipes!!", 'neg'),
        ("I wasn't really impressed with this! It was way too smokey, and it was kind of greasy. It's not something you want to make when you are craving a piece of chicken cuz it just falls apart. I actually used the chicken in a salad and it was good that way.", 'neg'),
        ("I give this recipe 2 stars for being easy to prepare but only 1 for taste.  It was bland and greasy  My family did not like it at all.", 'neg'),
        ("I found the flavor of this very bland, not at all what I had expected.", 'neg'),
        ("I have to say this recipe didn't go over really well at my house. I really wanted to to turn out well too! It just wasn't a flavor my family liked that well. Plus it had a very strong smokey flavor in the house all day. I would also like to make the comment that the chicken should be salted, and I NEVER add extra salt to things. I think part of it was that the fryer chicken we got ended up being pretty greasy. I've used fryers before, but they haven't ever really turned out like this. I think the only reason I gave it as many stars as I did was just because it was so easy to throw it together. I used the extra juice to make the rice like someone else commented, but I couldn't even eat any of it...flavor was just too strong.", 'neg'),
        ("I didn't want to put a star on this recipe, because I made quite a few changes in my version, but I just wanted to say that the basic idea here is great. I'd never heard of putting matzo balls in soup until I saw this recipe and now I think it's got to be the only way to go.", 'neg'),
        ("I&#039;m not sure who has tried this recipe but I followed each step with the exact ingredients. I crushed the corn flakes up to bread crumb consistency, and check the temp on my grease and it was on point. The cornflakes burnt within a minute of being in the fryer! They tasted horrible and burnt also. Ruined a whole pound of chicken! ?", 'neg'),
        ("I used to work for Zaxby's and pretty much none of these ingredients were used in making the strips", 'neg'),
        ("This recipe tastes like garbage! followed the directions to the letter, this is no where close to zaxbys chicken fingers!!!", 'neg'),
        ("I made this tonight, and the flavors do not complement each other at all, in my opinion.  I was disappointed.  I didn't eat much of it at all, because it really didn't appeal to me.  The combination of lemon, oregano and garlic didn't do the portobello mushrooms justice.  ", 'neg'),
        ("As written this was HORRIBLE. So sour we could not eat it, opened all fully canned jars to re can and add tripple the amount of sugar. I am wondering if the typeof plums used made any difference, The only thing i can think of is the skins on the plums maybe made the sauce more sour. The plums here in nova scotia are quite sour at times. they were so ripe however they fell apart in my hands when pitting them. EXCLUDE the vinegar, and add double the sugar. Base the sugar and vinegar amounts on the sourness/sweetness of the first plum mixture.", 'neg'),
        ("It was below my expectations. It tasted somewhat....sugary. To make it somewhat pleasant I added oregano, A LOT of pepper, and garlic salt. I could still taste the sugarnness. I'm not hard to please and don't mean to be unkind, but this recipe wasn't that good.", 'neg'),
        ("I was disappointed in this recipe.  First of all, I found a pie dish to be much too small.  I had to use a 2 qt. dish.  Second, I think the apples and the bread needed to be mixed together and not layered.  I think it would have come out better that way.  I will do that next time.  The overall flavor was pretty good.  Not my favorite recipe.", 'neg'),
        ("Sorry, this casserole didn't have enough flavor for me.  My grandson, who loves corn dogs didn't even care for it.", 'neg'),
        ("Hate to disappoint everyone, but this is not the original Famous Barr&#039;s French Onion Soup Recipe. Living very close to St. Louis, I had a friend who worked downtown making the French Onion Soup.  It was a (2) day process to make, but well worth the time it took. I have the original recipe but promised my friend I would never give it out.", 'neg'),
        ("I wish I could give 0 stars. This is a horrible version of this and was a waste of time and money. The proportion of Parmesan cheese is way off. It should be more like 1/4 cup than 2 3/4 cups", 'neg'),
        ("Unfortunatly, I have to rate this very low.  I followed the recipe exactly as it is written and it just was not good.  (I used Cod.)  Not one of us was able to eat it.  The fish was perfectly cooked...just the flavor of the breading was not good.", 'neg'),
        ("Sorry- we just thought these were dry, plain, and tasteless.  My DH is usually polite, but even he made a negative comment about these.  I made them almost exactly as stated (the only change I made was to cut the salt in half) so I'm not sure why we weren't as thrilled as the other reviewers.  Anyway, thanks for sharing, but we'll just have to keep looking for that ideal biscuit recipe.", 'neg'),
        ("Greatly disappointed. They were rather blase and flavorless. Even added cinnamon and vanilla to give it some flavor and it still didn&#039;t work. I was hoping for more.", 'neg'),
    ]
    test = [
        (
        'Delicious!!! Great flavour and easy to prepare - this was a hit with the family. My only problem with the recipe is that you didnot state a temperature for the oven - I baked at 180C for about 40 minutes. Thanks for a great meal and good luck!!!',
        'pos'),
        ('Excellent dish.  The topping is wonderfully rich and really makes the dish!', 'pos'),
        (
        'WOW!!! If I can please everyone at my table it is got to be GOOD.  This chicken had a wonderful flavor and was so simple to prepare.  Thank you.',
        'pos'),
        (
        'I hate to be the bad apple in the bunch but my entire family was very disappointed. We thought the flavor was too bland. I ended up heating some soy/ginger sauce up and pouring it over it so that we could eat it. Very disappointed.',
        'neg'),
        ('I am tired of this stuff.', 'neg'),
        (
        "I'm sorry, but I followed the directions exactly. The chicken was extremely tender, but the taste was worse than bland. I am using the leftovers in a casserole tonight. I will use the general idea again, but put seasoning on the chicken first. Thanks for sharing your recipe; maybe it's just a difference of taste!",
        'neg'),
        (
        "Neither my kids or my husband were dazzled by this.  I made a pot pie out of the leftovers but the initial chicken was not a winner",
        'neg'),
        (
        "We were expecting a chicken with more of a jerk heat but were not disappointed. We like our jerked chicken with skin so I did not use boneless skinless chicken. The topping was very good and I would suggest doubling it!!! yummy!!! Good luck Chef!",
        'pos'),
        (
        "Delicious!!  Made to the recipe apart from cutting my chicken into largish chunks. Great flavour and easy to prepare - this was a hit with the family. My only problem with the recipe is that you didn't state a temperature for the oven - I baked at 180C for about 40 minutes. Thanks for a great meal and good luck!!!",
        'pos'),
        (
        "We loved this chicken, even the picky daughter. The jerk rub did just as you said and filled the house with lovely smells! For the topping I used 3 cloves of garlic, (we love garlic!), and 1 jalapeno. I didn't need to let the sauce thicken on the stove. It thickened nicely in the oven. The chicken baked for 45 minutes, (the chicken breasts were large), and came out moist and perfectly cooked. I will be making up a quantity of the jerk rub for future use! Great recipe! ",
        'pos'),
        (
        "Ok last night I decided I wanted chicken so I came to zaar to seek out one of the RSC recipes and I found a true winner. I did not have the habanero pepper but it still tasted nummy!! You cannot believe the wonderful smell that fills the house. Why have plain chicken again. The list of ingredients seems intimidating but it really not a huge task to add. Someone really put their thinking caps on for this one. I love it !!!",
        'pos'),
        (
        "I made this tonight, and the flavors do not complement each other at all, in my opinion.  I was disappointed.  I didn't eat much of it at all, because it really didn't appeal to me.  The combination of lemon, oregano and garlic didn't do the portobello mushrooms justice.  ",
        'neg'),
        (
        "As written this was HORRIBLE. So sour we could not eat it, opened all fully canned jars to re can and add tripple the amount of sugar. I am wondering if the typeof plums used made any difference, The only thing i can think of is the skins on the plums maybe made the sauce more sour. The plums here in nova scotia are quite sour at times. they were so ripe however they fell apart in my hands when pitting them. EXCLUDE the vinegar, and add double the sugar. Base the sugar and vinegar amounts on the sourness/sweetness of the first plum mixture.",
        'neg'),
        (
        "It was below my expectations. It tasted somewhat....sugary. To make it somewhat pleasant I added oregano, A LOT of pepper, and garlic salt. I could still taste the sugarnness. I'm not hard to please and don't mean to be unkind, but this recipe wasn't that good.",
        'neg'),
        (
        "I was disappointed in this recipe.  First of all, I found a pie dish to be much too small.  I had to use a 2 qt. dish.  Second, I think the apples and the bread needed to be mixed together and not layered.  I think it would have come out better that way.  I will do that next time.  The overall flavor was pretty good.  Not my favorite recipe.",
        'neg'),
        (
        "Sorry, this casserole didn't have enough flavor for me.  My grandson, who loves corn dogs didn't even care for it.",
        'neg'),
        (
        "Hate to disappoint everyone, but this is not the original Famous Barr&#039;s French Onion Soup Recipe. Living very close to St. Louis, I had a friend who worked downtown making the French Onion Soup.  It was a (2) day process to make, but well worth the time it took. I have the original recipe but promised my friend I would never give it out.",
        'neg'),
        (
        "I wish I could give 0 stars. This is a horrible version of this and was a waste of time and money. The proportion of Parmesan cheese is way off. It should be more like 1/4 cup than 2 3/4 cups",
        'neg'),
        (
        "Unfortunatly, I have to rate this very low.  I followed the recipe exactly as it is written and it just was not good.  (I used Cod.)  Not one of us was able to eat it.  The fish was perfectly cooked...just the flavor of the breading was not good.",
        'neg'),
        (
        "Sorry- we just thought these were dry, plain, and tasteless.  My DH is usually polite, but even he made a negative comment about these.  I made them almost exactly as stated (the only change I made was to cut the salt in half) so I'm not sure why we weren't as thrilled as the other reviewers.  Anyway, thanks for sharing, but we'll just have to keep looking for that ideal biscuit recipe.",
        'neg'),
        (
        "Greatly disappointed. They were rather blase and flavorless. Even added cinnamon and vanilla to give it some flavor and it still didn&#039;t work. I was hoping for more.",
        'neg')
    ]

    cl = NaiveBayesClassifier(train)
    sent.pre = cl.classify(df)
    sent.percent = cl.accuracy(test)
    sent.percent = round(sent.percent, 2)
    sent.percent *= 100
    left = 100-sent.percent

    labels = 'Accuracy', 'Unreliable'
    sizes = [sent.percent, left]
    explode = (0.1, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    sent.show = plt.show()

    return render(request, "sentiment.html",{'sent':sent});

def show(request):
    final = Calorie()
    final.desire = des
    i = final.desire
    rec = int(i)
    connect = pg2.connect(database='food', user='postgres', password='0786')
    query = "SELECT * FROM raw_recipe"
    df = pd.read_sql(query, con=connect)
    df = pd.DataFrame(df, columns=['id', 'name', 'minutes', 'calories', 'fat', 'sugar', 'sodium', 'protein', 'saturated_fat', 'carbohydrates', 'description', 'n_ingredients', 'ingredients', 'ingredients', 'n_steps', 'steps'])
    df = df[df['id'] == rec]
    df = df.head(1)
    headers = ['Id', 'Name', 'Minutes', 'Calories', 'Fat', 'Sugar', 'Sodium', 'Protein', 'Saturated_Fat', 'Carbohydrates', 'Description', '# of Ingredients', 'Ingredients', 'Ingredients', '# of Steps', 'Steps']
    table = tabulate(df, headers, tablefmt="fancy_grid", showindex=False)
    final.show = table
    return render(request, "show.html",{'final':final});
