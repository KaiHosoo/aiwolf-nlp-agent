"""狂人のエージェントクラスを定義するモジュール."""

from __future__ import annotations

from aiwolf_nlp_common.packet import Role

from agent.agent import Agent


class Possessed(Agent):
    """狂人のエージェントクラス."""

    def __init__(
        self,
        config: dict,
        name: str,
        game_id: str,
        role: Role,  # noqa: ARG002
    ) -> None:
        """狂人のエージェントを初期化する."""
        super().__init__(config, name, game_id, Role.POSSESSED)
        self.fake_results = []  # 嘘の占い結果を記録
        self.claimed_seer = False
        self.co_possessed = False

    def talk(self) -> str:
        """トークリクエストに対する応答を返す."""
         # 1日目の最初に偽の占い師CO
        if self.game_day == 1 and not self.claimed_seer:
            self.claimed_seer = True
            return f"COMINGOUT {self.agent_name} SEER"

        # 1〜2日目に嘘の占い結果を報告
        if self.game_day in [1, 2] and len(self.fake_results) < self.game_day:
            fake_target = self._choose_fake_target()
            fake_result = "HUMAN" if self.game_day == 1 else "WEREWOLF"
            self.fake_results.append((fake_target, fake_result))
            return f"DIVINED {fake_target} {fake_result}"

        # 3日目に真占い師が脱落していたら狂人CO
        if self.game_day == 3 and not self.co_possessed and self._true_seer_dead():
            self.co_possessed = True
            return f"COMINGOUT {self.agent_name} POSSESSED"

        return "OVER"
        #return super().talk()

    def vote(self) -> str:
        """投票リクエストに対する応答を返す."""
        # 占い結果に従って投票（最新の結果の対象に投票）
        if self.fake_results:
            return self.fake_results[-1][0]

        # 3日目に狂人CO後は村人に投票（村人と思われる候補から選ぶ）
        if self.co_possessed:
            return self._choose_villager_candidate()
        
        return super().vote()
    
    # 以下は内部ロジック（仮実装）
    def _choose_fake_target(self) -> str:
        """嘘の占い対象を選ぶ（自分と人狼以外）"""
        candidates = [
            agent
            for agent in self.other_agents
            if agent != self.agent_name and agent not in self.werewolf_team
        ]
        return sorted(candidates)[0] if candidates else self.other_agents[0]

    def _true_seer_dead(self) -> bool:
        """真の占い師が死んでいるかどうかをチェック（仮の実装）"""
        return "Seer_Player" in self.dead_agents  # プレースホルダ名

    def _choose_villager_candidate(self) -> str:
        """村人っぽい人を選んで投票する（仮の実装）"""
        candidates = [
            agent
            for agent in self.other_agents
            if agent not in self.werewolf_team and agent not in self.dead_agents
        ]
        return sorted(candidates)[0] if candidates else self.other_agents[0]
