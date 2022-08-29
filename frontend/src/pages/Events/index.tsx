import * as React from "react";
import ReactDOM from 'react-dom';
import { Layout } from "../../components/template/Layout";




const EventsPage: React.FC = () => {

  return (
    <Layout content={<></>} rPanel={{
      visible: false,
      open: false,
      content: undefined
    }}></Layout>    
  )
}

export {EventsPage}