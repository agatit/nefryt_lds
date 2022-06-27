import * as React from "react";
import { Link } from "react-router-dom";
import { Layout } from "../../components/template/Layout";





const EditorPage: React.FC = () => {

  return (
    <Layout rPanel={{open:false, visible:false, 
      content:<></> 
    }} content={
    <div className={'root'}>
      Editor
      <nav>
          <ul>
            <li>
              <Link to="/">Home</Link>
            </li>
            <li>
              <Link to="/editor">Edytor</Link>
            </li>
            <li>
              <Link to="/events">Zdarzenia</Link>
            </li>
            <li>
              <Link to="/charts">Wykresy</Link>
            </li>
          </ul>
        </nav>
    </div>
    }/>
  )
}

export {EditorPage}