Select player_id, player_name AVG(pts) AS avg_pts
FROM gamedetails
WHERE season = 2022
GROUP BY player_id
HAVING AVG(pts) > 25
ORDER BY avg_pts DESC;

Select
  gd.season, t.nickname,
  ROUND(AVG(gd.fg3m), 2) AS avg_3ptrs
from gamedetails gd
join playerdetails pd ON gd.player_id = pd.player_id
join teams t ON gd.team_id = t.team_id
where pd.player_name = 'Stephen Curry'
group by gd.season, t.nickname
order by gd.season;

Select g.season,g.home_team_id,t.nickname, 
COUNT(*) as home_wins
from games g
join teams t ON g.home_team_id = t.team_id
where g.home_team_wins = True
group by g.season, g.home_team_id, t.nickname
having COUNT(*) = (
  select MAX(wins)
  from (
    select COUNT(*) as wins from games
    where home_team_wins = True AND season = g.season
    group by home_team_id
  ) as season_wins
)order by g.season;

select g.game_date_est, g.season, g.home_team_id, th.nickname as home_team, rh.w as home_wins, rh.l as home_losses, g.visitor_team_id, tv.nickname as visitor_team, rv.w as visitor_wins, rv.l as visitor_losses 
from games g join teams th on g.home_team_id = th.team_id join teams tv on g.visitor_team_id = tv.team_id join ranking rh on rh.team_id = g.home_team_id and rh.standingsdate = g.game_date_est join ranking rv on rv.team_id = g.visitor_team_id and rv.standingsdate = g.game_date_est
where ((g.home_team_id = 1610612747 and g.visitor_team_id = 1610612738) or (g.home_team_id = 1610612738 and g.visitor_team_id = 1610612747)) 
order by g.game_date_est desc limit 5;

select pd.player_name, avg_pts.player_id, round(avg_pts.avg_points, 2) as avg_points
from (
  select player_id, avg(pts) as avg_points
  from gamedetails
  group by player_id
  having avg(pts) > (
    select avg(pts) from gamedetails
  )
) as avg_pts
join playerdetails pd on pd.player_id = avg_pts.player_id
order by avg_pts.avg_points desc
limit 10;

select 
  pd.player_name, 
  avg_pts.player_id, 
  round(avg_pts.avg_points, 2) as player_avg, 
  round(global_avg.overall_avg, 2) as overall_avg
from (
  select player_id, avg(pts) as avg_points
  from gamedetails
  group by player_id
) as avg_pts
join playerdetails pd on pd.player_id = avg_pts.player_id
join (
  select avg(pts) as overall_avg from gamedetails
) as global_avg on true
where avg_pts.avg_points > global_avg.overall_avg
order by avg_pts.avg_points desc
limit 10;

select pd.player_name, round(avg(gd.pts),2) as player_avg, 
       (select round(avg(pts),2) from gamedetails where season=2017) as season_avg
from gamedetails gd
join playerdetails pd on gd.player_id = pd.player_id
where gd.season = 2017
group by pd.player_name
having avg(gd.pts) > (select avg(pts) from gamedetails)
order by player_avg desc
limit 10;




