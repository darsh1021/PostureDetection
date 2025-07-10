import { useNavigate } from "react-router-dom";

function Live()
{
    const navigate = useNavigate();
    function squat()
    {
        navigate("/WebCamSquat");
    }

    function back()
    {
        navigate("/WebCamBack");
    }

    return(<>
     <div className="page-container">
  <h1 className="main-heading">Choose Streaming Way </h1>

  <div className="button-group">
    <button className="custom-button" onClick={squat}>Squats</button>
    <button className="custom-button" onClick={back}>Desk Sitting</button>
  </div>
</div>
    </>);
}

export default  Live; 