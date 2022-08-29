import { Button } from "@material-ui/core";
import * as React from "react";
import ReactDOM from 'react-dom';
import { useNavigate } from "react-router-dom";
import { useListTrendsQuery } from "../../store/trendApi";



const ChartsPage: React.FC = () => {
  const navigate = useNavigate();
  const { data, error, isLoading } = useListTrendsQuery();
  console.log(data);
console.log(error);
console.log(isLoading);
const handleClick = async () => {
    
  
    
  navigate('/');
   
   
};

  return (
    <div className={'root'}>
      Charts
      <Button onClick={handleClick} variant="contained">Home</Button>
    </div>
  )
}

export {ChartsPage}