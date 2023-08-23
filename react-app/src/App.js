import React, { useState, useEffect } from "react";
import { useDispatch } from "react-redux";
import { Route, Switch } from "react-router-dom";
import SignupFormPage from "./components/SignupFormPage";
import LoginFormPage from "./components/LoginFormPage";
import { authenticate } from "./store/session";
import Navigation from "./components/Navigation";
import SpotGetter from "./components/Spots/GetAllSpots";
import CurrentSpotDetails from "./components/Spots/GetASpot";
import Chat from "./components/DirectMessage/directmessage";
import MessageThreads from "./components/MessageThreads/messagethreads";

function App() {
  const dispatch = useDispatch();
  const [isLoaded, setIsLoaded] = useState(false);
  useEffect(() => {
    dispatch(authenticate()).then(() => setIsLoaded(true));
  }, [dispatch]);

  return (
    <>
      <Navigation isLoaded={isLoaded} />
      {isLoaded && (
        <Switch>
          <Route path="/login" exact={true}>
            <LoginFormPage />
          </Route>

          <Route path="/signup" exact={true}>
            <SignupFormPage />
          </Route>

          <Route path='/' exact={true}>
            <SpotGetter/>
          </Route>
          <Route path='/selectedSpot/:spotId' exact={true}>
            <CurrentSpotDetails/>
          </Route>
          <Route path='/directmessage/:userId/:ownerId' exact={true}>
            <Chat/>
          </Route>
          <Route path='/test' exact={true}>
            <MessageThreads/>
          </Route>
        </Switch>
      )}
    </>
  );
}

export default App;
