import * as React from "react";
import ReactDOM from 'react-dom';
import { Layout } from "../../components/template/Layout";
import { EditorContent } from "./content";
import "./style.css";



const EditorPage: React.FC = () => {

  return (
    <Layout content={<EditorContent></EditorContent>} rPanel={{
      enable: false,
      open: false,
      content: undefined,
      handleDrawer: undefined
    }}></Layout>    
  )
}

export {EditorPage}