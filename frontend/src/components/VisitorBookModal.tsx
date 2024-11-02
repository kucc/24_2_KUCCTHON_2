import React, { useState, useEffect } from "react";
import sign from '../img/Sign.svg';
import banana from '../img/banana.svg';
import styles from "./VisitorBookModal.module.css";
import axios from 'axios';

interface Comment {
  user_name: string;
  content: string;
  created_at: string;
}

interface planet {
  user_name:string;
  content:string;
  created_at:string;
}


interface PlanetResponse {
  planet_name: string;
  user_name: string;
  comments: planet[];
  count: number
}

interface VisitorBookProps {
  userId: number;
  setUserId: (id: number) => void;
  otherId: number;
}

const VisitorBookModal: React.FC<VisitorBookProps> = ({ userId, setUserId, otherId }) => {
  const [word, setWord] = useState('');
  const [comments, setComments] = useState<Comment[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [planets, setPlanets] = useState<planet[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  // Comment 작성 함수
  const useCreateComment = async (otherId: number) => {
    try {
      const response = await axios.post(
        `http://127.0.0.1:8000/planet/${encodeURIComponent(otherId)}/comments`,
        {
          current_user_id: userId,
          content: word,
        },
        {
          withCredentials: true,
        }
      );
      if (response.data.success) {
        alert(response.data.message);
        console.log(otherId)
        setWord(''); // 성공 후 입력 필드를 비웁니다.
        await fetchVisitor();
      } else {
        alert('Failed to add comment.');
        console.log(otherId)
      }
    } catch (error) {
      console.error(error);
    }
  };

  // Comments 가져오는 함수
  const fetchVisitor = async (): Promise<PlanetResponse> => {
    const response = await fetch(`http://127.0.0.1:8000/planet/${otherId}/comments`, {
      method: "GET",
    });
  
    if (!response.ok) {
      throw new Error("Network response was not ok " + response.statusText);
    }
  
    const data = await response.json();
    console.log(response)
    console.log(otherId)
    return data;
  }

  useEffect(() => {
    const getPlanets = async () => {
      try {
        const data = await fetchVisitor();
        setPlanets(data.comments); // planets state에 data 할당
      } catch (err) {
        // err를 Error 타입으로 단언
        if (err instanceof Error) {
          setError(err.message); // 오류 메시지 설정
        } else {
          setError("An unknown error occurred");
        }
      } finally {
        setLoading(false); // 로딩 상태 해제
      }
    };

    getPlanets();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  const handleCreate = () => {
    // eslint-disable-next-line react-hooks/rules-of-hooks
    useCreateComment(otherId);
    setWord('')
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault(); // Enter 시 줄바꿈 방지
      handleCreate();
    }
  };

  return (
    <div>
      {/* <div className={styles.sign}>
        <img src={sign} alt="이미지" />
      </div> */}
      <div className={styles.textContainer}>
        <div className={styles.textbox}>
          <textarea
            className={styles.textarea}
            placeholder="친구 우끼에게 소식을 남겨요 (로딩에 시간이 걸립니다 ㅠㅠ 새로고침 한 번 해보는 것두?)"
            onChange={(e) => setWord(e.target.value)}
            onKeyDown={handleKeyDown}
            value={word}
          />
          <img
            className={styles.sendBtn_red}
            role="presentation"
            src={banana}
            alt="submit"
            onClick={handleCreate}
          />
        </div>
      </div>
      <div className={styles.VisitorList}>
        {error ? (
          <div>{error}</div>
        ) : (
          planets.map((comment) => (
            <div className={styles.comment}>
              <p><strong>{comment.user_name}</strong></p>
              <p>{comment.content}</p>
              <p className={styles.date}>{new Date(comment.created_at).toLocaleString()}</p>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default VisitorBookModal;
