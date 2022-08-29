import * as React from "react";
import ReactDOM from 'react-dom';
import { Layout } from "../../components/template/Layout";




const NoPageFound: React.FC = () => {

  return (
    <Layout content={<></>} rPanel={{
      enable: false,
      open: false,
      content: undefined,
      handleDrawer: undefined
    }}></Layout>    
  )
}

export {NoPageFound}