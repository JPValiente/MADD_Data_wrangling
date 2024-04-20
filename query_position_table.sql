----- Position Table
-- Position Table
select * from (
select  *, dense_rank () over (partition by season, league_id order by pts desc, gd) lugar
from   (
select  season, league_id, team_api_id,
		sum(GP) GP,
		sum(W) W,
		sum(D) D,
		sum(L) L,
		sum(GF) GF,
		sum(GA) GA,
		sum(GF - GA) GD,
		sum(3*W + 1*D) PTS
from (
--- Local
select  season, league_id, team_api_id,
		sum(GP) GP,
		sum(W) W,
		sum(D) D,
		sum(L) L,
		sum(GF) GF,
		sum(GA) GA
from (
select 	season, league_id, 1 GP, 
		home_team_api_id team_api_id,
        (case when home_team_goal > away_team_goal then 1 else 0 end) W,
        (case when home_team_goal = away_team_goal then 1 else 0 end) D,
        (case when home_team_goal < away_team_goal then 1 else 0 end) L,
        home_team_goal GF,
        away_team_goal GA
from    "Match"
)
group by  season, league_id, team_api_id
--
union all
--- Away
select  season, league_id, team_api_id,
		sum(GP) GP,
		sum(W) W,
		sum(D) D,
		sum(L) L,
		sum(GF) GF,
		sum(GA) GA
from (
select 	season, league_id, 1 GP, 
		away_team_api_id team_api_id,
        (case when home_team_goal < away_team_goal then 1 else 0 end) W,
        (case when home_team_goal = away_team_goal then 1 else 0 end) D,
        (case when home_team_goal > away_team_goal then 1 else 0 end) L,
        away_team_goal GF,
        home_team_goal GA
from    "Match"
)
group by  season, league_id, team_api_id
)
group by  season, league_id, team_api_id
)
)
;
---------
--- Local
---------
select * 
from 
(
select  season, league_id, team_api_id,
		sum(GP) GP,
		sum(W) W,
		sum(D) D,
		sum(L) L,
		sum(GF) GF,
		sum(GA) GA
from (
select 	season, league_id, 1 GP, 
		home_team_api_id team_api_id,
        (case when home_team_goal > away_team_goal then 1 else 0 end) W,
        (case when home_team_goal = away_team_goal then 1 else 0 end) D,
        (case when home_team_goal < away_team_goal then 1 else 0 end) L,
        home_team_goal GF,
        away_team_goal GA
from    "Match"
)
group by  season, league_id, team_api_id
) a
left join 
(
select * from team 
) b
on a.team_api_id = b.team_api_id

;
---------
--- Away
---------
select  season, league_id, team_api_id,
		sum(GP) GP,
		sum(W) W,
		sum(D) D,
		sum(L) L,
		sum(GF) GF,
		sum(GA) GA
from (
select 	season, league_id, 1 GP, 
		away_team_api_id team_api_id,
        (case when home_team_goal < away_team_goal then 1 else 0 end) W,
        (case when home_team_goal = away_team_goal then 1 else 0 end) D,
        (case when home_team_goal > away_team_goal then 1 else 0 end) L,
        away_team_goal GF,
        home_team_goal GA
from    "Match"
)
group by  season, league_id, team_api_id

;

