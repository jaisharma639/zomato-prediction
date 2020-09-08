# zomato-prediction

Overview

ZPL ( _Zomato Premier League)_ lets user predict sports outcome and rewards them with appropriate rewards at the end of each such match. The app has following features:

- Select match and answer from a list of questions.
- User administration - All basic user functions like login, signup, session management.
- Interact with a third party api (like _cricbuzz_) to fetch live match data.
- A reward system based on the accuracy of user chosen options. Reward is given in the form of zomato credits.
- Leaderboad to show the highest credit earners.
- My activity page to track all questions a user has answered and corresponding rewards earned.
- A notification system to let users know about the contest completion and credits they earned during the contest.
- Share about ZPL with friends.
- A pluggable eligibility criteria that can be configured per question. This eligibility decides the credits a user scores for a particular question-answer combination.
- An admin interface to modify questions, add answers, alter eligibility.

The app runs on Django and uses SQLite for storing the data with the flexibility to plugin any other data store like PostgeSQL, MongoDB etc. The entire architecture is built using Model-view-controller architectural pattern.

Storage

The following models are used to power the app. Please note that all of the following models use &quot;id&quot; as the primary key which is autoincremented.

1. User

User model is implemented by django. Django takes care of session management along with storing few key information bits like the following:

_auth\_user_

| **Name** | **Type** |
| --- | --- |
| username | varchar(150) |
| email | varchar(254) |
| password | varchar(128) |
| first\_name | varchar(30) |
| last\_name | varchar(30) |

2. Active Matches

Stores the information for all active (ongoing) matches in the system. The information is updated/deleted based on data updates in partner at a given polling frequency. The table also has a reference to match id being fetched from partner.

_activematches_

| **Name** | **Type** |
| --- | --- |
| match\_text | varchar(50) |
| match\_id | smallint unsigned |
| match\_completed | bool |

3. Question

Each match will have certain set of questions to be entered by admin. Stores the correct answer for each question along with the type of question (multiple correct/single correct).

_question_

| **Name** | **Type** |
| --- | --- |
| question\_text | varchar(200) |
| correct\_ans | varchar(20) |
| match\_id | Foreign key(Active Matches) |
| question\_type | varchar(1) |

4. Choice

Admin entered choices for a given question to be displayed in the contest.

_choice_

| **Name** | **Type** |
| --- | --- |
| question\_id | Foreign key (Question) |
| choice\_text | varchar(200) |

5. Participants

All information for currently ongoing contest goes here. It stores the answers committed by each user during the contest and then updates the rewards once the contest ends.

_participants_

| **Name** | **Type** |
| --- | --- |
| chosen\_ans | smallint unsigned |
| question\_id | Foreign key (Questions) |
| user\_field\_id | Foreign key (User) |
| reward | smallint unsigned |

6. Activity

This table is a copy of _Participants_ table except the fact that its never cleaned up (for the sake of My activity page). Also, this table doesn&#39;t have foreign key to Active Matches and thus cleanup doesn&#39;t purge entries from this table.

_activity_

| **Name** | **Type** |
| --- | --- |
| information | varchar(200) |
| reward | smallint unsigned |
| user\_field\_id | Foreign key (User) |

API specs

The admin dashboard can be accessed by navigating to /admin. The following endpoints are exposed for the app. Note that all endpoints have to be prefixed with /predict.

| **Endpoint** | **Params** | **Description/Response** |
| --- | --- | --- |
| / | GET | List of all active matches rendered as html |
| /\&lt;match\_id\&gt; | GET | List of questions for given match rendered as html |
| /question/\&lt;question\_id\&gt; | GET | List of choices as an html POST form |
| /answer/\&lt;question\_id\&gt; | POST {&quot;choice&quot; : [2,3,4] } | Submit chosen answer for given user. _Response_ : HttpResponse |
| /my\_activity | GET | Display question along with reward that the user has answered as html |
| /leaderboard | GET | Show top credit earners as html |
| /login | GET | Display login form |
| /signup | GET/POST | Display signup form if GET else signup the user using signup form. |
| /logout | GET | Logs user out.Response - HttpResponse |
| /password\_reset | GET | Display password reset form. |

Sequence Diagram

![](RackMultipart20200908-4-qjd9qs_html_ddd9443321f94d7e.png)

Enhancements

The following areas can be improved/optimized for making the app scalable, fault-tolerant and for better user experience :

- Use of cache : The participants table suffers major load once a match completes. All relevant rows for a particular contest have to be updated. This number can be few million sometimes. Use of an in-memory data structure like Redis or Memcached can be made to keep active contest entries in memory and thus calculating rewards in memory. This cache can be persisted to Participants db through an asynchronous call during non-peak hours.
- Task submission like that of updation of rewards and sending out notifications should be handled through a queuing mechanism. Celery can be used in such cases for maintaining a queue of tasks to be executed concurrently &amp; asynchronously on different worker nodes. Celery uses multiprocessing and thus tasks can be batched and distributed among different threads/pools.
- System has to be fault tolerant and should have failover mechanism. The following questions can be asked:
  - What happens when redis cache collapses on service crash?
**A :** Rebuild the entire data structure from primary db.
  - What if a match completes and our system is unable to update the same?
**A :** Cease all sequential updates/changes in the system. The design should be in a way that the entire operation from match completion till notifications are sent out should be atomic.
- Use cron job for tracking updates in the partner data. The crontab expression can be configured as per the need. This will send regularly schedules HTTP GET requests to the given partner and would scan for changes.
- Choice table should have uniqueness on text stored so as to restrict admin from entering same choice twice.
- Admin UI can be enhanced for smooth experience by showing questions next to match and choices next to question. For more customizations, new wrapper views need to be implemented on top of Django admin apis.
