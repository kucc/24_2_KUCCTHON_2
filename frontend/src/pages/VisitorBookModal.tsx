import React from "react";
import ReactDOM from "react-dom/client";
import styles from "./Planet.module.css";
import sign from '../img/Sign.svg'

const VisitorBookModal: React.FC = () => {
    return (
      <div className={styles.background}>
        <div>
          <img src={sign} alt='이미지' />
        </div>
        <div>
            
        </div>
      </div>
    );
  };
  
  export default VisitorBookModal;
  