import {useState} from "react";
import ReactDOM from "react-dom/client";
import styles from "./Planet.module.css";
import planet from '../img/Planet.svg'
import VisitorBookModal from "./VisitorBookModal";

const Planet: React.FC = () => {

  const [isClick, setIsClick] = useState(false)

  const handleClick = () => {
    console.log('클릭됨')
    setIsClick(!isClick)
  }

  return (
    <div className={styles.background}>
      <div>
        <img src={planet} alt='이미지' />
      </div>
      <div className={isClick? styles.modal : styles.hidden}>
          <VisitorBookModal/>
      </div>
      <button className={styles.modalBtn} onClick={handleClick}>Modal열기</button>
    </div>
  );
};

export default Planet;
