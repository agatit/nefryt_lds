import * as React from "react";
import ReactDOM from 'react-dom';
import { Layout } from "../../components/template/Layout";
import { EditorContent } from "./content";
import { useListNodesQuery} from "../../store/nodeApi";
import "./style.css";
import { useListLinksQuery } from "../../store/linkApi";



const EditorPage: React.FC = () => {

  //console.log('AAAAAAAAAAAAAAAAAAAAAAAA');
  var filter={};
  useListNodesQuery(filter);
  useListLinksQuery(filter);
  
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