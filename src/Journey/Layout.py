from enum import Enum
from Journey.Scene import Scene
from Journey.TreasureScene import TreasureScene
from Journey.Circumstance import Circumstance, Circumstances
from Generation.selection import Selector, NonRepSelector

class Difficulty(Enum):
    Easy = 0
    Normal = 1
    Hard = 2
    Challenging = 3

class Layout:
    """
    The Layout class represents a level of the game, composed of various scenes generated based on Circumstances.
    Circumstances encapsulate small fragments of information about the context of the scenes, enabling descriptions such as "You are in a forest" or "You have killed xyz".

    The scenes within this layout generate Circumstances upon completion, which are subsequently spread to establish tighter connections between the scenes.
    This mechanism fosters a network of interrelated information, enhancing the coherence and continuity of the level.
    """
    _DIFFICULTY_PROBABILITIES = {
        Difficulty.Easy: 0.5,
        Difficulty.Normal: 0.3,
        Difficulty.Hard: 0.15,
        Difficulty.Challenging: 0.05
    }

    # TODO: implement scenes: emptyscene, battlescene, dialoguescene, ?, ?, ?, ...
    _SCENE_PROBABILITIES = {
        TreasureScene: 1.0
    }

    _SCENE_SELECTOR_LAMBDA = 0.5

    def __init__(self, 
                 number_of_scenes: int,
                 max_depth_of_intuition: int,
                 min_difficulty: Difficulty,
                 max_difficulty: Difficulty,
                 general_intuitions: Circumstances):
                # TODO: Maybe some kind of context should also be added and an endgoal for the layout... I'm not entierely sure about the generation yet
        """
        Constructor for the Layout class.

        Parameters:
        - number_of_scenes (int): The maximum number of scenes that will be generated for this layout.
        - max_depth_of_intuition (int): The maximum depth where an circumstance can be spread to. For instance, if this value is 3 and a scene at index 5 wants to spread an circumstance, that circumstance can spread at most to the 8th scene.
        - min_difficulty (Difficulty): The minimum difficulty of any scene that will be generated.
        - max_difficulty (Difficulty): The maximum difficulty of any scene that will be generated.
        - general_intuitions (Circumstances): Circumstances applied to every scene in this layout. For example, this can contain location-related circumstances.
        """
        self._number_of_finished_scenes = 0
        self._max_depth_of_intuition = max_depth_of_intuition
        self._scenes: list[Scene] = [None] * number_of_scenes
        
        # The general circumstance is added to every scene
        self._intuitions_for_scenes = [[circumstance for circumstance in general_intuitions]] * number_of_scenes

        # Init difficulty selector
        if min_difficulty.value < max_difficulty.value:
            min_difficulty, max_difficulty = max_difficulty, min_difficulty

        possible_difficulties = [Difficulty(i) for i in range(min_difficulty.value, max_difficulty.value + 1)]
        possible_difficulty_probabilities = [Layout._DIFFICULTY_PROBABILITIES[i] for i in possible_difficulties]

        self._difficulty_selector = Selector(possible_difficulties, possible_difficulty_probabilities)

        # Init scene selector
        self._scene_selector = NonRepSelector(list(Layout._SCENE_PROBABILITIES.keys()),
                                              list(Layout._SCENE_PROBABILITIES.values()),
                                              Layout._SCENE_SELECTOR_LAMBDA)

    @property
    def last_scene(self) -> Scene | None:
        """
        Retrieve the last generated scene or None if no scene has been generated yet.

        Returns:
        - Scene | None: Returns the last generated Scene object, or None if no scene has been generated yet.
        """
        return self[self._number_of_finished_scenes]

    @property
    def max_number_of_scenes(self) -> int:
        """
        Retrieve the maximum number of scenes that can be generated for this layout.

        Returns:
        - int: The maximum number of scenes that can be generated for this layout.
        """
        return len(self._scenes)
    
    @property
    def number_of_finished_scenes(self) -> int:
        """
        Retrieve the maximum number of scenes that can be generated for this layout.

        Returns:
        - int: The maximum number of scenes that can be generated for this layout.
        """
        return self._number_of_finished_scenes


    def __getitem__(self, index) -> Scene | None:
        """
        Retrieve the Scene at the specified index or None if the Scene has not been generated yet.

        Parameters:
        - index (int): The index of the Scene to retrieve.

        Returns:
        - Scene | None: Returns the Scene object at the specified index if it has been generated; otherwise, returns None.
        """
        return self._scenes[index]

    def create_next_scene(self) -> Scene | None:
        """
        Generate the next scene in the layout and return it according to defined rules.

        Returns:
        - Scene | None: Returns the next generated Scene or None based on specific rules.

        Note:
        This method generates the subsequent scene in the layout based on certain conditions:
            - If no scenes have been generated yet, it generates the initial scene, which is always an EmptyScene describing the context.
            - If scenes exist, it checks if the last scene is completed. If not, it returns the last scene.
            - If the last scene is completed and not the final scene, it generates a new one and returns it.
            - If the last scene is completed and is the final scene, it returns None.
        """
        # Check if the previous scene is finished
        last_scene = self._scenes[self._number_of_finished_scenes]
        if last_scene is None:
            # This is the first scene 
            pass
        elif last_scene.is_finished:
            self._number_of_finished_scenes += 1
            next_scene_type = self._scene_selector()
            next_scene_difficulty = self._difficulty_selector()
            # TODO
            pass

        return None

    def spread_intuition(self, scene_index: int, circumstance: Circumstance, count: int = 1) -> None:
        """
        Spread the given circumstance that originates from the specified scene_index. The count parameter determines the maximum number of scenes
        to which this circumstance should be propagated. The depth of the spread is regulated by the object's max_depth_of_intuition.
        
        Parameters:
        - scene_index (int): The index identifying the scene where the circumstance originates.
        - circumstance (Circumstance): The circumstance object to be spread among scenes.
        - count (int): The maximum number of scenes to which the circumstance will be propagated. Defaults to 1.

        Returns:
        - None
        """
        # Obtain all possible indices of scenes where circumstance can be spread to
        indices = list(range(scene_index + 1, max(len(self._scenes, scene_index + self._max_depth_of_intuition))))

        # Sort them by their number of circumstances in an increasing order
        indices.sort(key=lambda x: len(self._intuitions_for_scenes[x]))

        for i in range(min(count, len(indices))):
            self._intuitions_for_scenes[indices[i]].append(circumstance)

