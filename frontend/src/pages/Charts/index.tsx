import { Button } from "@material-ui/core";
import * as React from "react";
import ReactDOM from 'react-dom';
import { useNavigate } from "react-router-dom";
import { Layout } from "../../components/template/Layout";
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
    <Layout content={<></>} rPanel={{
      visible: false,
      open: false,
      content: undefined
    }}></Layout>    
  )
}

export {ChartsPage}