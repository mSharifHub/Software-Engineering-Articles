import datetime

post_dummydata = [
    {
        "slug": "apis-in-practice",
        "image": "api-post-image.png",
        "author": "Mohamed Sharif",
        "date": datetime.date(2024, 4, 1),
        "title": "Api in practice",
        "content": """
    repository -> https://github.com/mSharifHub/googleMapsPinLocation

 When it comes to API's is like playing with Legos. There are set of golden rules that API developers must follow so it can make easier for us to use. As far as now, I found one book REST API Design Rulebook, by O'Reilly Media, Inc with about 112 pages. I think would be good time spending to learn the golden rules. API's follow a REST architecture which means Representation State Transfer. Basically, is like placing an order to a pizza place. You tell all the need to know and they will deliver the order to you. The catch is that after you place the order, the second time you place another order the restaurant does not know anything about you anymore. The good advantage is that it maintains simplicity and scale horizontally since any server can handle any request at any time without needing access to share data. And there are more reasons to why an API follow a REST architecture of our World Wide Web. 
 As you start to figuring out that writing code from scratch is like reinventing the wheel every time you can leverage from public API's. There are so many but here we will be using google maps. Google maps offers a very easy sign up process and documentation to use Google API's. It would be such great learning journey building our own map and algorithms and put in practice well know algorithms like Dijkstra, Bellman-Ford, Bidirectional Search, and many more. Yet, the reality is that would be a pain ~/.@$$. Graph algorithms are hard and applying into a real application is even harder. Per say, hard is not hard but is time consuming. That goes back to the reason why not abstract what we do not need and focus in what we want. So, after learning to leverage API's it should not be difficult to start using other API providers since most follow a similar practice and documentation. 
 Lets start with google maps API. So, the bad news, and trust me I am doing this for free and by no means advertising google. I think it should be indeed free but is not. To use certain API's we need to pay. For google we need to pay about $25 dollars for a developer account. But, if you ever have explore swift world and the apple developer community, the price tag for apple is at $90 -$100 dollars. There are I believe free maps API that I have not explored. So, to create an account we go to google developer account and I don't need to even to explain because google console walk you through the whole process. You need to create a project and I recommend put a budge alert. I believe they give $300 credit to utilize their API and should be enough to learn and build projects on git. But I will go trough in not using the console but actually using google cloud services locally in our machine. So, depending on the system you are using it will vary the installation and location installed. If you have a mac you cam simply type
 brew install --cask google-cloud-sdk
gcloud --version
to install it and confirm installation. then we need to login. If you ever used aws cli is very similary as well. Google gcloud will take us to login in the console.
gcloud auth login
if you do not want the browser and go hard code on just command prompt then go for 
gcloud init --no-launch-browser
you simply put your credentials. After we need to generate an api key to use in our application
gcloud alpha services api-keys create --project  <name>
and we need to enable 
gcloud services enable --project <name>  "maps-backend.googleapis.com"
more on this on https://cloud.google.com/sdk/gcloud/reference/services/enable.
The process might not be as straight forward but check console and all need is confirm you have a project, you have an api key, and enable the service you want to use in your project.
Now this is the fun part. in this example, I am using a react vite project template with typescript. After you do the installing, do the usual clean up or you can install the minimum using flags. 
Walk through the logic
 import './App.css'
import {Status as GoogleMapsStatus, Wrapper} from "@googlemaps/react-wrapper";
import Map from "./components/Map";
function App() {

  const render = (status: GoogleMapsStatus | null)=>{
    if (status === "LOADING") {

      return <h1> loading map ....</h1>
    }
     if ( status === "FAILURE") {

      return <h1> failure</h1>
    }
    else{
      return <Map/>
    }
  }

  return (
    <>
    <div>
      <Wrapper apiKey={import.meta.env.VITE_GOOGLE_API_KEY}render ={render}>
      </Wrapper>
    
    </div>
    </>
  )
}

export default App 
So, this is the app.tsx or app.js file. first we need to install 

 npm i @googlemaps/react-wrapper @googlemaps/markerclusterer
 npm i -D @types/google.maps
 we need to check the status which is 
export enum Status {     LOADING = "LOADING",     FAILURE = "FAILURE",     SUCCESS = "SUCCESS", }
Each state is nice to let the user know and if success then we just return the map. the map here is a component made and not a google library. We then use Wrapper
A component to wrap the loading of the Google Maps JavaScript API.
import { Wrapper } from '@googlemaps/ react-wrapper';

const MyApp = () => (
	<Wrapper apiKey={'YOUR_API_KEY'}>
		<MyMapComponent />
	</ Wrapper>
);
the api key that you have insert and include render so to return the state.

Now lets jump to the map component
import {useEffect, useRef, useState} from "react";

export default function Map() {
    const [map, setMap] = useState<google.maps.Map>();
    const [circle, setCircle] = useState<google.maps.Circle>();
    const ref = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (ref.current && !map) {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition((position) => {
                    const pos = {
                        lat: position.coords.latitude,
                        lng: position.coords.longitude,
                    };
                    const initialConfig = {
                        center: pos,
                        zoom:10,
                    };
                    const newMap = new window.google.maps.Map(ref.current as HTMLDivElement , initialConfig);
                    setMap(newMap);
                    const radiusCircle = new google.maps.Circle({
                        strokeColor: "blue",
                        strokeOpacity: 0.8,
                        strokeWeight: 1,
                        fillColor: "blue",
                        fillOpacity: 0.10,
                        map: newMap,
                        center: pos,
                        radius: 100, // meters
                    })

                    setCircle(radiusCircle);
                }, (error) => {
                    console.error('Geolocation error:', error);
                });
            }

        }
    }, [ map]);




    useEffect(() => {
        if (map) {
            const maxZoom = 20;
            let zoomLevel = map.getZoom();
            const zoomInQuickly = () => {
                if (zoomLevel !== undefined && zoomLevel < maxZoom) {
                    map.setZoom(++zoomLevel); // Increment and set the zoom level
                    setTimeout(zoomInQuickly, 200); // Set the next zoom step to occur quickly
                }
            };

            zoomInQuickly(); // Start the zooming process
        }
    }, [map]);


    useEffect(() => {
        if (circle){
            let radius = 300;
            const minRadius = 100;
            let focusing = true

            const interval = setInterval(()=>{
                if (focusing){
                    radius -= 10

                    if ( radius <= minRadius){
                        focusing = false
                    }
                }


                circle.setRadius(radius)
            },50)

            return ()=> clearInterval(interval)
        }
    }, [circle]);

    return(
        <>
        <div ref={ref} style={{height: "100%", width: "75vw", minHeight:"75vh"}}></div>
        </>
    )
    
}

so we need a state so set a map and use the map state and generic type will be google.maps.Map. Also, we need a radius circle to show in the map our radius location instead of just a pin. We will do the same but utilize .Circle. Also, I have a ref to directly refer to the DOM since google needs refer it directly to host the map or a better word to serve as a container to the map.

So, we have 3 useEffects and is simply one for the actual location and to create a map, the second for the radius animation and the last is map focus animation. The most important of course is the first one where the base functionality is.
We check ref.current and if map have not being created, in a better way is hey if we have the reference to the element and the map have not being created then we will do the following. Now, we need to get the user location. For that, we will use navigation.geolocation. We then get our current position, we set the center of zoom level and then we create a map and set our state to the map we just created. 
The other 2 logic is just to robust our application to make more fun.
however, I noticed an issue on -> WRONG 

useEffect(() => {
    if (map) {
        const maxZoom = 20;
        let zoomLevel = map.getZoom();
        const zoomInQuickly = () => {
            if (zoomLevel !== undefined && zoomLevel < maxZoom) {
                map.setZoom(++zoomLevel); // Increment and set the zoom level
                setTimeout(zoomInQuickly, 200); // Set the next zoom step to occur quickly
            }
        };

        zoomInQuickly(); // Start the zooming process
    }
}, [map]);

and we can change to -> CORRECT 
useEffect(() => {
    let timeOut:ReturnType<typeof setTimeout>
    if (map) {
        const maxZoom = 20;
        let zoomLevel = map.getZoom();
        const zoomInQuickly = () => {

            if (zoomLevel !== undefined && zoomLevel < maxZoom) {
                map.setZoom(++zoomLevel); // Increment and set the zoom level
            timeOut = setTimeout(zoomInQuickly, 200); // Set the next zoom step to occur quickly
            }
        };

        zoomInQuickly(); // Start the zooming process
    }
    return ()=> clearTimeout(timeOut)
}, [map]);
so the time out does not continue to run after the component is unmounted. 

Finally, we need to to have a div to refer to and add the style . The div will be the container where the map will be displayed. 

Moral of Story
There are so many applications we can build by leveraging from APIS and at same time learn in depth. It feels like playing with Lego. I mean the whole concept of programming is just like legos. For example, we could build an application that leverage different APIS, where we have our phone contacts, music providers, map, etc.. The opportunities are endless . Yet, I will and would recommend still to get in depth and learn or revise graphs. This is on my bucket list to do. Graph algorithms! But, starting with arrays and as in fact being very good with arrays should be a good start point. Continue to build and practice your programming skills sets so it can grow exponentially . If you like thumbs up and good Sunday 

        """
    },

]
