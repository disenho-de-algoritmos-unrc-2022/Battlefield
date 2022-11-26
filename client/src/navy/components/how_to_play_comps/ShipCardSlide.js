import React, { useEffect, useState } from "react";
import NavyTitle from ".././NavyTitle";
import Destroyer from "../../assets/Destroyer.png";
import Cruiser from "../../assets/Cruiser.svg";
import Battleship from "../../assets/Battleship.svg";
import Corvette from "../../assets/Corvette.svg";
import "../../../index.css";

import MissileService from "../../services/MissileService";
import ".././NavyShip.css";

const ShipCardSlide = ({ ship, name }) => {
  const [missiles, setMissiles] = useState({});

  useEffect(() => {
    MissileService.getMissileTypes().then((resp) => {
      const missiles = resp.data.data;
      ship.missile_type_id.forEach((id) => {
        if (missiles[id]) {
          setMissiles((prev) => ({ ...prev, [id]: missiles[id] }));
        }
      });
    });
  }, []);

  const getShipImage = () => {
    switch (name) {
      case "Destroyer":
        return Destroyer;
      case "Cruiser":
        return Cruiser;
      case "Battleship":
        return Battleship;
      case "Corvette":
        return Corvette;
      default:
        return null;
    }
  };

  return (
    <div className="navy-card-ship-container-small d-flex flex-column align-items-center border border-dark py-3 mt-1 mb-3 ">
      <div
        className="navy-text w-100 d-flex justify-content-center"
        style={{ fontSize: "14px" }}
      >
        {name}
      </div>

      <div className="w-75 d-flex justify-content-around align-items-center py-3">
        <img
          src={getShipImage()}
          alt="Ship"
          style={{ width: "100px", height: "auto" }}
        />
      </div>

      <div className="w-60 d-flex">
        <div className="d-flex flex-column align-items-center">
          <p className="navy-text" style={{ margin: "0px" }}>
            Hp: {ship.hp}
          </p>

          <p className="navy-text" style={{ margin: "0px" }}>
            Size: {ship.size}{" "}
          </p>
          <p className="navy-text" style={{ margin: "0px" }}>
            Speed: {ship.speed}
          </p>
          {Object.keys(missiles).map((key) => {
            return (
              <div key={key}>
                <p className="navy-text" style={{ margin: "0px" }}>
                  Missile Type: {key}
                </p>

                <p className="navy-text" style={{ margin: "0px" }}>
                  Damage: {missiles[key].damage}
                </p>
                <p className="navy-text" style={{ margin: "0px" }}>
                  Speed: {missiles[key].speed}
                </p>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default ShipCardSlide;
