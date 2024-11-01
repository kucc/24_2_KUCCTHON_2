import React from "react";
import ReactDOM from "react-dom/client";
import paper from '../img/paper.svg'
import Button from "../components/Button";
import styles from "./PickupModal.module.css";

const PickupModal: React.FC = () => {
    const handlePickUp =() => {
        
    }
    return (
      <div className={styles.pickUpContaioner}>
        <div className={styles.paper}>
          <img src={paper} alt='이미지' />
        </div>
        <div className={styles.Btn}>
            <Button text='바나나 사용하기' onClick={handlePickUp}/>
            {/* <img src={아이템 그림} />
            <p>{아이템 이름}</p> */}
        </div>
      </div>
    );
  };
  
  export default PickupModal;
  