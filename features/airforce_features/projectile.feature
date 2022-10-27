Feature: Creation, movement of a projectile

    @air_force_projectile
    Scenario: Player_a join in a new game
        Given a users logged
        When  user_a create the game
        And add a plane
        Then a '200' responses

    @air_force_projectile
    Scenario: Player_b join in a new game 
        Given a users logged
        When user_b enter the game
        And add his plane
        Then get '200' response
    
     @air_force_projectile
     Scenario: Player_a create a projectile
          Given player_a in the map
          When player_a create a projectile
          Then '200' response
        
    @air_force_projectile
    Scenario: Player_b create a projectile
        Given player_b in the map
        When player_b create a projectile
        Then a '200' response 

    
    # @air_force_projectile
    # Scenario: Player_b create a projectile
    #     Given player_a and player_b in the game with their planes and projectiles available
    #     When player_b create projectile
    #     Then get a '200' response

#     # @air_force_projectile
#     # Scenario: Player_a projectile motion
    #     Given projectile of player_a in the battlefield
    #     When a new turn starts and the projectiles of player_a have to be updated
    #     Then the projectiles of player_a moves the speed corresponding

    # @air_force_projectile
    # Scenario: Player_b projectile motion
#     #     Given a projectile of player_b in the 
#     #     When a new turn starts and the projectiles of player_b have to be updated 
#     #     Then the projectile of player_b moves the speed corresponding

    # @air_force_projectile
    # Scenario: Projectile collision
    # Given two or more projectile in the battlefield
    # When a collision occurs
    # Then a '200' response

 