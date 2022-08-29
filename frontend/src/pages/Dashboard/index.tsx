import { Button } from "@material-ui/core";
import * as React from "react";
import ReactDOM from 'react-dom';
import { useNavigate } from "react-router-dom";
import { AuthLoginApiArg, useAuthLoginMutation } from "../../store/authApi";
import { useListTrendsQuery } from "../../store/trendApi";




const DashboardPage: React.FC = () => {
  const navigate = useNavigate();
  const [
    updateloginPost, // This is the mutation trigger
    { isLoading: isUpdating }, // This is the destructured mutation result
  
  ] = useAuthLoginMutation()
var isAuth=false;

  
  
 const { data, error, isLoading } = useListTrendsQuery();
 console.log(data);
console.log(error);
console.log(isLoading);

  const handleClick = async () => {
    
  
  
   navigate('/charts');
    
    
};

const handleTrendClick = async () => {
    

  
  
};


  return (
    <div className={'root'}>
      <div>Daschboard</div>
      <Button onClick={handleClick} variant="contained">Charts</Button>
      
                  
    </div>
    
  )
}

export {DashboardPage}