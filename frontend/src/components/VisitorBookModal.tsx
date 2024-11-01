import React from "react";
import ReactDOM from "react-dom/client";
import sign from '../img/Sign.svg'
import styles from "./VisitorBookModal.module.css";

const VisitorBookModal: React.FC = () => {
    return (
      <div>
        <div className={styles.sign}>
          <img src={sign} alt='이미지' />
        </div>
        <div>
            
        </div>
      </div>
    );
  };
  
  export default VisitorBookModal;
  