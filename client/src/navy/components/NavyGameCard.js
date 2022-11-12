import React, { useEffect, useState } from "react";
import wings from "./../assets/wings.svg";
import NavyButton from "./NavyButton";
import NavyUserCard from "./NavyUserCard";
import "./NavyGameCard.css";
import authService from "../../services/auth.service";
import NavyGameService from "../services/NavyGameService";
import { useNavigate } from "react-router-dom";

const NavyGameCard = ({ game }) => {
  const [user1, setUser1] = useState({});
  const [user2, setUser2] = useState({});
  const navigate = useNavigate();
  const currentUser = authService.getCurrentUser();

  const canJoin = () => {
    return (
      !(currentUser.sub !== game.user_1.id && currentUser.sub !== user2.id) ||
      freeToJoin()
    );
  };

  const freeToJoin = () => {
    return Object.keys(user2).length === 0;
  };

  const joinPlayer = () => {
    if (freeToJoin()) {
      if (currentUser.sub === game.user_1.id) {
        navigate(`/navy/games/${game.id}/lobby`);
      } else {
        NavyGameService.patchNavyGame(game.id).then((res) => {
          navigate(`/navy/games/${game.id}/lobby`);
        });
      }
    } else if (game.ready_to_play) {
      navigate(`/navy/games/${game.id}/board`);
    } else {
      navigate(`/navy/games/${game.id}/ship_selection`);
    }
  };

  const canReJoin = () => {
    const currentUser = authService.getCurrentUser();
    return (
      currentUser.sub === game.user_1.id || currentUser.sub === game.user_2.id
    );
  };

  useEffect(() => {
    if (game.user_2) {
      setUser2(game.user_2);
    }
  }, []);

  return (
    <div className="navy-card-container d-flex flex-column align-items-center border border-dark pt-2 pb-4">
      <p className="navy-text m-0">{game.id}</p>
      <div className="w-100 d-flex justify-content-center mb-2">
        <img src={wings} alt="Wings" />
      </div>
      <div className="w-75 d-flex justify-content-around align-items-center">
        <NavyUserCard username={game.user_1.username} />
        <p className="navy-text">VS.</p>
        <NavyUserCard
          username={Object.keys(user2).length !== 0 ? user2.username : ""}
          rol={Object.keys(user2).length !== 0 ? "guest" : "free"}
        />
      </div>
      {canJoin() ? (
        <div className="text-center">
          <NavyButton action={joinPlayer} text={"join"} size={"small"} />
        </div>
      ) : null}
    </div>
  );
};

export default NavyGameCard;
