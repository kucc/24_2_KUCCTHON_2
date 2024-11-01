import React, { useState } from 'react';
import styles from "./Blackhole.module.css";
import blackhole from "../img/blackhole.svg";
import blackhole_hover from "../img/blackhole_hover.svg";


interface BlackholeProps {
text?:string;
onClick?: () => void; 
}
const Blackhole: React.FC<BlackholeProps> = ({onClick,text}) => {

  return (
    <div className={styles.background}>
<div className={styles.blackholeContainer}>
<img src={blackhole} alt="blackhole" className={styles["button-image"]} />
<img
  src={blackhole_hover}
  alt="blackhole hover"
  className={styles["button-hover-image"]}
  onClick={onClick}
/>
<span className={styles["blackhole-text"]}>{text}</span>
</div>
       </div>
  );
};

export default Blackhole;
