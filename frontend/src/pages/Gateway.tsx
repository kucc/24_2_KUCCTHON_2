import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from "./Gateway.module.css";
import Blackhole from "../components/Blackhole";
import star_blue from "../img/star_blue.svg";
import star_yellow from "../img/star_yellow.svg";
import star_pink from "../img/star_pink.svg";
import star_violet from "../img/star_violet.svg";


interface GatewayProps {
text?:string;
onClick?: () => void; 
userId: number;
setUserId: (id: number) => void;
}

const Gateway: React.FC<GatewayProps> = ({onClick,text,userId, setUserId}) => {
  const navigate = useNavigate(); 
  const handleStarClick = () => {
    navigate("/channel"); 
  };

  const handleBlackholeClick = () => {
    const planetUserId = userId;
    navigate(`/planet/${planetUserId}`);
  };

  return (
    <div className={styles.background}>
      <div className={styles.starContainer}>
      <div className={styles.star_pinkContainer}>
      <img src={star_pink} alt="star_pink"  className={styles.star} onClick={handleStarClick}/>
      <span className={styles.starText}>삼각형자리 </span>
      </div>  
      <div className={styles.star_yellowContainer}>
      <img src={star_yellow} alt="star_yellow"  className={styles.star} onClick={handleStarClick}/>
      <span className={styles.starText}>안드로메다</span>
      </div>
      <div className={styles.star_blueContainer}>
      <img src={star_blue} alt="star_blue"  className={styles.star} onClick={handleStarClick}/>
      <span className={styles.starText}>우리 은하</span>
      </div>
      <div className={styles.star_violetContainer}>
      <img src={star_violet} alt="star_violet"  className={styles.star} onClick={handleStarClick}/>
      <span className={styles.starText}>IC 1101</span>
      </div>
      </div>
<div className={styles.centerContainer}>
  <Blackhole text='내 행성' onClick={handleBlackholeClick} />

</div>
       </div>
  );
};

export default Gateway;
