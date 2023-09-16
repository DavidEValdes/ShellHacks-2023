import React from 'react';
import { GoogleLogin } from 'react-google-login';

function App() {
  const responseGoogle = (response) => {
    if (response.tokenId) {
      fetch("/process_emails", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ token: response.tokenId }),
      })
      .then(res => res.json())
      .then(data => {
        console.log(data); // You can display these data in your components
      });
    }
  };

  return (
    <div className="App">
      <GoogleLogin
        clientId="YOUR_GOOGLE_CLIENT_ID"
        buttonText="Login with Google"
        onSuccess={responseGoogle}
        onFailure={responseGoogle}
      />
    </div>
  );
}

export default App;