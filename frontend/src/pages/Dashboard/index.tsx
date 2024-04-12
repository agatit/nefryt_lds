import { Button } from "@material-ui/core";
import * as React from "react";
import ReactDOM from 'react-dom';
import { useNavigate } from "react-router-dom";
import { AuthLoginApiArg, useAuthLoginMutation } from "../../store/authApi";
import { useListTrendsQuery } from "../../store/trendApi";
import { Layout } from "../../components/template/Layout";



const DashboardPage: React.FC = () => {
  const navigate = useNavigate();
  const [
    updateloginPost, // This is the mutation trigger
    { isLoading: isUpdating }, // This is the destructured mutation result
  
  ] = useAuthLoginMutation()
var isAuth=false;

  
  
 //const { data, error, isLoading } = useListTrendsQuery();
 //console.log(data);
//console.log(error);
//console.log(isLoading);

  const handleClick = async () => {
    
  
  
   navigate('/charts');
    
    
};

const handleTrendClick = async () => {
    

  
  
};


  return (
    <Layout content={<></>} rPanel={{
      enable: false,
      open: false,
      content: undefined,
      handleDrawer: undefined
    }}></Layout>    
  )
}

export {DashboardPage}