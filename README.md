## Inspiration

While traveling to ShellHacks, a conversation I had with my carpool buddies became the spark for this idea. We discussed the numerous internship applications I had submitted and the method I employed to streamline the process using Notion. Amid this conversation, an epiphany struck — I realized that I could leverage my prior experience with the OpenAI API to make this internship tracking endeavor even more efficient.

## What it does

Upon initiation, the application dives into your Gmail, specifically scanning the content of your last 10 emails. With the help of OpenAI's GPT-4 API, it analyses the content to determine the relevance of each email in the context of your job or internship search. Whether it's an acceptance, rejection, or a follow-up, InternTrack categorizes them efficiently for you.

## How I built it

The core foundation of InternTrack rests upon two powerful APIs: Gmail and OpenAI's GPT-4. To stitch these technologies together and craft a seamless user experience, I opted for Python and Flask for the backend operations. For the frontend, React provided the dynamic interface, while Axios handled the API requests, bridging the gap between the front and backend.

## Challenges I ran into

One of the most prominent challenges I faced was managing and routing the tokens efficiently. Furthermore, crafting the logic behind the Python script was no simple feat. However, after rigorous debugging and a timely mentorship session, the issues were ironed out, and accurate results started pouring in.

## Accomplishments that I am proud of

Beyond the technical feats, what truly fills me with pride is the journey itself. The very fact that I took an abstract idea and, within a span of 36 hours, transformed it into a fully functional web application stands as a testament to sheer willpower and dedication.

## What I learned

Apart from gaining a deeper understanding of various Python libraries, I explored the intricacies of hosting a Flask server within a virtual environment. Additionally, the project gave me insights into diverse methods of front and backend interactions, many of which were previously unknown to me.

## What's next for InternTrack

InternTrack, in its current form, is built with scalability in mind. The choice to limit the scan to 10 emails was deliberate, ensuring the system remains within API rate and token limits. However, as technology evolves and API call costs decrease, this limitation can be revisited. The groundwork has been laid, and with further development, InternTrack can become an indispensable tool for job seekers everywhere.
